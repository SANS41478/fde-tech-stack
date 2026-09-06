---
title: Agent Loop 深度拆解 — ReAct 循环的源码级讲解
aliases:
  - Agent Loop
  - ReAct 循环
  - ReactLoopAgent
tags:
  - deepseek-harness
  - agent-loop
  - react
created: 2026-08-31
---

# Agent Loop 深度拆解 — ReAct 循环的源码级讲解

> [!tip] 目标
> 从源码级别理解 Agent Loop 的完整执行流程。这是 Harness 最核心的部分——所有其他组件都围绕它运转。

---

## 1. 整体流程图

Agent Loop 是 Harness 的"心脏"，下面是它的完整流程：

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Loop                            │
│                                                         │
│  ┌──────────────────────────────────────────────┐       │
│  │ 用户输入到达                                   │       │
│  └──────────────┬───────────────────────────────┘       │
│                 ▼                                       │
│  ┌──────────────────────────────────────────────┐       │
│  │ 消息进入 Inbox（消息队列）                      │       │
│  │ 有两个队列：next-turn 和 next-step             │       │
│  └──────────────┬───────────────────────────────┘       │
│                 ▼                                       │
│  ┌──────────────────────────────────────────────┐       │
│  │ wakeDriver() — 唤醒驱动器                      │       │
│  │ 如果当前是 idle，启动一个 driver                │       │
│  └──────────────┬───────────────────────────────┘       │
│                 ▼                                       │
│  ┌──────────────────────────────────────────────┐       │
│  │ kick() — 主循环                               │       │
│  │   while (await this.turn()) {}                │       │
│  └──────────────┬───────────────────────────────┘       │
│                 ▼                                       │
│  ┌──────────────────────────────────────────────┐       │
│  │ turn() — 一个轮次                              │       │
│  │                                              │       │
│  │   记录 turn/start                             │       │
│  │   while(true):                               │       │
│  │     preStep() ─→ 组装上下文                    │       │
│  │         │                                    │       │
│  │         ▼                                    │       │
│  │     step() ─→ 调用 LLM + 执行工具             │       │
│  │         │                                    │       │
│  │         ▼                                    │       │
│  │     检查是否需要继续                            │       │
│  │         │                                    │       │
│  │         ├─ 有新消息 → 继续循环                  │       │
│  │         └─ 无新消息 → 退出循环                  │       │
│  │                                              │       │
│  │   记录 turn/end                               │       │
│  └──────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Phase 状态机

Agent 有三种状态，就像交通灯：

```
         ┌─────────────┐
         │    idle     │ ← 没有工作，等待消息
         │   （绿灯）   │
         └──────┬──────┘
                │ 收到消息，wakeDriver()
                ▼
         ┌─────────────┐
         │   running   │ ← 正在执行 turn/step
         │   （红灯）   │
         └──────┬──────┘
                │ 工作完成
                ▼
         ┌─────────────┐
         │    idle     │ ← 回到等待状态
         │   （绿灯）   │
         └─────────────┘

         另外还有一种：
         ┌─────────────┐
         │ maintenance │ ← 维护期间（如热重载配置）
         │   （黄灯）   │
         └─────────────┘
```

在源码中（`agent.ts:38-46`）：

```typescript
type Phase =
  | { kind: 'idle'; lastTurn: number }
  | { kind: 'maintenance'; abort: AbortController; lastTurn: number; wakeRequested: boolean }
  | { kind: 'running'; abort: AbortController; turn: number; step: number; wakeRequested: boolean }
```

> [!tip] 类比
> - `idle` = 你在等快递，没事做
> - `running` = 你正在拆快递，很忙
> - `maintenance` = 你在整理房间，快递来了先放门口

---

## 3. preStep — 组装上下文

`preStep` 是每一步的**准备工作**：

```
preStep()
  │
  ├─ [1] inbox.claim() — 从队列取出消息
  │      从 next-turn 或 next-step 队列取消息
  │
  ├─ [2] systemPrompt.assemble() — 组装系统提示
  │      把以下内容拼在一起：
  │      - 系统提示（Agent 的人格和规则）
  │      - 工具列表（每个工具的名称和描述）
  │      - 注入的上下文（插件添加的额外信息）
  │
  ├─ [3] renderContextSections() — 渲染上下文段落
  │      把组装好的内容渲染成文本
  │
  ├─ [4] agent/pre-step 事件 — waterfall
  │      插件可以在这里：
  │      - 修改消息内容
  │      - 注入额外上下文
  │      - 拒绝某些消息（reject）
  │
  └─ [5] 返回准备结果
         kind: 'enter' → 继续执行
         kind: 'reject' → 拒绝，结束 turn
```

在源码中（`agent.ts:225-243`）：

```typescript
private async preStep(target: InboxTarget, position: { turn: number; step: number }): Promise<PreparedStep> {
  // 1. 取出消息
  const claimed = this.inbox.claim(target, position.turn)

  // 2. 组装系统提示
  const assembly = await this.loopCtx.systemPrompt.assemble(assembleContextFor(this, signal))

  // 3. 渲染上下文
  const sections = renderContextSections(assembly)
  const context = this.runtimeContext.project(joinContextSections(sections), sections)

  // 4. 触发 waterfall，插件可以修改
  const decision = await this.dispatch.waterfall(
    'agent/pre-step', { messages: claimed, ...position, signal },
    (): Promise<PreStepDecision> => Promise.resolve<PreStepDecision>({
      kind: 'enter',
      messages: context === undefined ? claimed : [...claimed, context],
    }),
  )

  // 5. 返回结果
  return decision.kind === 'reject' ? decision : { ...decision, assembly }
}
```

---

## 4. step — 调用 LLM + 执行工具

`step` 是每一步的**核心工作**：

```
step(assembly)
  │
  ├─ [1] renderPrompt() — 渲染系统提示
  │      把组装好的内容渲染成 LLM 能理解的格式
  │
  ├─ [2] buildRequest() — 构建请求
  │      确定用哪个模型、什么参数
  │
  ├─ [3] llm.stream() — 流式调用 LLM
  │      发送请求，逐 token 接收回复
  │
  ├─ [4] 记录 assistant/chunk — 每个 token 一个事件
  │      用于回放和 UI 显示
  │
  ├─ [5] 组装完整回复
  │      把所有 token 拼成完整消息
  │
  ├─ [6] 判断回复类型
  │      │
  │      ├─ 有工具调用 → executeToolCalls()
  │      │              → 执行工具
  │      │              → 工具结果放入 next-step 队列
  │      │              → 返回 null（继续循环）
  │      │
  │      └─ 无工具调用 → 返回 'completed'（结束循环）
  │
  └─ [7] 处理 max-tokens
         如果达到输出上限，返回 'max-tokens'
```

在源码中（`agent.ts:332-401`），关键部分：

```typescript
private async step(assembly: PromptAssembly): Promise<StepEndReason | null> {
  // ... 构建请求 ...

  while (true) {
    // 流式调用 LLM
    const stream = this.loopCtx.llm.stream(request)
    for await (const chunk of stream) {
      // 每个 token 都记录
      this.session.append('assistant/chunk', { turn, step, chunk })
      assembler.push(chunk)
    }

    // 组装完整消息
    const message = createAssistantMessage({ content: assembler.blocks() })
    this.session.append('assistant/message', { turn, step, message })

    // 检查是否有工具调用
    const toolCalls = message.content.filter(block => block.type === 'tool-call')
    if (toolCalls.length === 0) return { kind: 'completed' }  // 没有工具调用，结束

    // 执行工具调用
    const { concluded } = await executeToolCalls(
      this.loopCtx, turn, step, toolCalls, signal,
      context => this.inbox.splice('next-step', ..., [context]),  // 结果放入队列
    )
    return concluded ? { kind: 'completed' } : null  // null = 继续循环
  }
}
```

---

## 5. Inbox 双队列机制

Agent 有两个消息队列，就像邮箱里的两个格子：

```
┌─────────────────────────────────────────┐
│  Inbox                                   │
│                                         │
│  ┌─────────────┐  ┌─────────────┐       │
│  │ next-turn   │  │ next-step   │       │
│  │ 下一轮处理   │  │ 当前轮处理   │       │
│  └─────────────┘  └─────────────┘       │
│                                         │
│  规则：                                  │
│  - next-step 的消息优先处理               │
│  - next-turn 的消息等当前轮结束后处理      │
└─────────────────────────────────────────┘
```

**为什么需要两个队列？**

| 场景 | 放哪个队列 | 原因 |
|---|---|---|
| 用户新消息 | next-turn | 等当前工作完成再处理 |
| 工具执行结果 | next-step | 马上需要处理，继续当前轮 |
| 注入的上下文 | next-step | 马上需要让 LLM 看到 |
| 紧急取消 | next-turn | 中断当前轮 |

在源码中：

```typescript
// 用户消息 → next-turn
send(message, target = 'next-turn', wakeup = true)

// 工具结果 → next-step
this.inbox.splice('next-step', ..., [context])
```

---

## 6. 取消与错误处理

### 取消（Cancel）

当用户点击"停止"或发送取消信号：

```
cancel(cause)
  │
  ├─ 清空 Inbox（如果 keepInbox=false）
  │
  └─ 触发 abort
     → 所有正在进行的 await 被中断
     → turn 记录 'aborted' 结束原因
     → driver 退出
```

### 错误处理

```
step() 执行过程中出错
  │
  ├─ LLM 调用失败
  │   → agent/request-error waterfall
  │   → 插件决定：retry 或 throw
  │
  ├─ 工具执行失败
  │   → 记录 tool/result (isError: true)
  │   → 错误信息作为工具结果返回给 LLM
  │   → LLM 看到错误后自行决定下一步
  │
  └─ 其他错误
      → 记录 turn/end (reason: error)
      → 错误信息发送给 agent/error 事件
      → driver 退出
```

---

## 7. 完整的 Turn 执行示例

让我们跟踪一个完整的 Turn：

```
用户输入："帮我写一个 hello world 的 Python 脚本"
  │
  ├─ [1] 消息进入 next-turn 队列
  │
  ├─ [2] wakeDriver() → 进入 running 状态
  │
  ├─ [3] turn() 开始
  │      记录 turn/start { turn: 1 }
  │
  ├─ [4] preStep()
  │      取出消息
  │      组装上下文：系统提示 + 工具列表 + 用户消息
  │      返回 { kind: 'enter', messages: [...] }
  │
  ├─ [5] step() 开始
  │      记录 step/start { turn: 1, step: 1 }
  │
  ├─ [6] buildRequest()
  │      确定模型：deepseek-chat
  │      记录 request/header
  │
  ├─ [7] llm.stream()
  │      流式接收：我 + 需要 + 使用 + bash + 工具...
  │      每个 token 记录 assistant/chunk
  │
  ├─ [8] 组装完整回复
  │      "我需要使用 bash 工具创建一个 Python 脚本"
  │      记录 assistant/message
  │
  ├─ [9] 识别工具调用
  │      tool-call: bash, arguments: "echo 'print(\"hello world\")' > hello.py"
  │
  ├─ [10] executeToolCalls()
  │       记录 tool/call
  │       执行 bash 命令
  │       记录 tool/result
  │       结果放入 next-step 队列
  │
  ├─ [11] step/end { turn: 1, step: 1 }
  │
  ├─ [12] 检查 next-step 队列 → 有消息，继续
  │
  ├─ [13] preStep()（第 2 步）
  │       取出工具结果
  │       组装上下文（包含工具结果）
  │
  ├─ [14] step()（第 2 步）
  │       记录 step/start { turn: 1, step: 2 }
  │       调用 LLM
  │       LLM 回复："我已经创建了 hello.py 文件"
  │       没有工具调用 → 返回 'completed'
  │       记录 step/end { turn: 1, step: 2 }
  │
  ├─ [15] 检查 next-step 队列 → 空，退出循环
  │
  ├─ [16] turn/end { turn: 1, reason: 'completed' }
  │
  └─ [17] 回到 idle 状态
```

---

## 8. 与其他组件的交互

Agent Loop 是中心枢纽，连接了几乎所有其他组件：

```
                    ┌──────────────┐
                    │  用户输入     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
         ┌─────────│  Agent Loop   │─────────┐
         │         │ (ReactLoop)  │         │
         │         └──────┬───────┘         │
         │                │                 │
         ▼                ▼                 ▼
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │ Session Log │  │    LLM      │  │   Tools     │
  │ （记录一切）  │  │ （大脑）     │  │ （手脚）     │
  └─────────────┘  └─────────────┘  └─────────────┘
         │                │                 │
         ▼                ▼                 ▼
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │   Inbox     │  │   Prompt    │  │   Sandbox   │
  │ （消息队列）  │  │ （上下文组装）│  │ （安全隔离）  │
  └─────────────┘  └─────────────┘  └─────────────┘
```

| 组件 | 与 Loop 的关系 |
|---|---|
| Session Log | Loop 每一步都写入日志 |
| LLM | Loop 调用 LLM 获取回复 |
| Tools | Loop 执行 LLM 请求的工具 |
| Inbox | Loop 从 Inbox 取消息，工具结果放回 |
| Prompt | Loop 组装上下文给 LLM |
| Sandbox | 工具在 Sandbox 中执行 |

---

## 小结

Agent Loop 的核心就是**一个 while 循环**：

```
while (有消息要处理) {
  1. 取消息
  2. 组装上下文
  3. 调用 LLM
  4. 如果有工具调用 → 执行工具 → 结果放回队列 → 继续
  5. 如果没有工具调用 → 结束
}
```

所有复杂性都来自于：如何处理并发、如何处理错误、如何处理取消、如何记录日志、如何让插件介入。

---


---

## 延伸阅读

本篇是 ReAct 循环的**源码级**讲解；循环背后的设计考量（上下文组装策略、KV Cache 友好布局、压缩与状态栏）见 [[上下文工程]]；Harness 的约束/验证/纠正分层见 [[Harness 工程]]。

---

## 下一步

理解了 Agent Loop 后，我们来看看它的"手脚"如何工作：[[08-工具系统]]。
