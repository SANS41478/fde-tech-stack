---
title: ReAct 深度解析与 Agent 架构层级详解
aliases:
  - ReAct 详解
  - Agent 架构层级
  - LLM vs Agent 边界
tags:
  - deepseek-harness
  - react
  - agent
  - 架构
created: 2026-08-31
type: tutorial
domain: ai
layer: implementation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# ReAct 深度解析与 Agent 架构层级详解

> [!tip] 本章目标
> 彻底讲清楚 ReAct 模式、Agent 的完整架构层级、Session Log 的本质、插件化的范围、多 Agent 的实现、安全设计的位置、流式 token 的含义、Goal 系统的作用。

---

## 一、ReAct 模式 — 从人类思考方式到代码实现

### 1.1 什么是 ReAct

> [!tip] 类比：你修自行车的过程
> ReAct = **Re**asoning + **Act**ing（推理 + 行动）
>
> 你修自行车时，大脑在做的事：
>
> ```
> 观察：车骑不动了
>   ↓
> 推理：可能是链条断了（Reasoning）
>   ↓
> 行动：检查链条（Acting）
>   ↓
> 观察：链条确实断了
>   ↓
> 推理：需要买新链条（Reasoning）
>   ↓
> 行动：去商店买（Acting）
>   ↓
> 观察：买到了
>   ↓
> 推理：现在装上（Reasoning）
>   ↓
> 行动：装链条（Acting）
>   ↓
> 观察：车能骑了 → 停止
> ```
>
> 关键：**每一步行动之后，你都会观察结果，然后重新推理下一步该做什么**。

### 1.2 ReAct vs 其他模式

| 模式 | 特点 | 缺点 |
|---|---|---|
| **纯推理**（Chain-of-Thought）| 只思考不行动 | 无法获取外部信息 |
| **纯行动**（Tool Calling）| 直接调用工具 | 没有思考过程 |
| **ReAct** | 推理和行动交替进行 | 需要多次 LLM 调用 |

### 1.3 ReAct 在 Harness 代码中的实现

Harness 的 `ReactLoopAgent`（`packages/core/agent-loop/src/agent.ts`）是 ReAct 的直接工程实现。

**核心循环结构**（`agent.ts:263`）：

```typescript
// turn() 方法里的核心循环
while (true) {                          // ← 无限循环，直到不需要继续
  const step = phase.step + 1

  // ──── Reasoning 阶段 ────
  const decision = await this.preStep(target, { turn, step })
  // preStep 做了什么？
  //   1. 从 Inbox 取出消息
  //   2. 组装上下文（系统提示 + 历史 + 工具列表）
  //   3. 触发 agent/pre-step waterfall（插件可以修改消息）
  //   4. 返回 { kind: 'enter', messages: [...] } 或 { kind: 'reject' }

  if (decision.kind === 'reject') break  // ← 被拒绝，结束

  // ──── Acting 阶段 ────
  this.session.append('step/start', { turn, step })
  for (const message of decision.messages) {
    this.session.append('user/message', message)  // ← 记录输入
  }

  const stepEnd = await this.step(decision.assembly)  // ← 执行一步

  this.session.append('step/end', { turn, step })     // ← 记录结束

  // ──── 观察结果，决定是否继续 ────
  if (turnEnds && this.inbox.nextStep.length === 0) break
  // 如果没有新消息了，退出循环
  target = 'next-step'  // ← 下一步从 next-step 队列取消息
}
```

**step() 方法——一次完整的"推理+行动"**（`agent.ts:332`）：

```typescript
private async step(assembly: PromptAssembly): Promise<StepEndReason | null> {
  while (true) {
    // ──── 1. 构建请求（准备给 LLM 看什么）────
    const { request } = await this.buildRequest(
      turn, step, assembly.tools, system,
      this.session.deriveMessages(),  // ← 从 Session Log 推导消息历史
      signal,
    )

    // ──── 2. 流式调用 LLM ────
    const stream = this.loopCtx.llm.stream(request)
    for await (const chunk of stream) {
      // 每个 token 都记录到 Session Log
      this.session.append('assistant/chunk', { turn, step, chunk })
      assembler.push(chunk)
    }

    // ──── 3. 组装完整回复 ────
    const message = createAssistantMessage({ content: assembler.blocks() })
    this.session.append('assistant/message', { turn, step, message })

    // ──── 4. 检查是否有工具调用 ────
    const toolCalls = message.content.filter(block => block.type === 'tool-call')

    if (toolCalls.length === 0) {
      return { kind: 'completed' }  // ← 没有工具调用，ReAct 循环结束
    }

    // ──── 5. 执行工具调用（Acting）────
    const { concluded } = await executeToolCalls(
      this.loopCtx, turn, step, toolCalls, signal,
      context => this.inbox.splice('next-step', ..., [context]),
      // ← 工具结果放入 next-step 队列
    )

    return concluded ? { kind: 'completed' } : null
    // null = 继续循环（回到 while(true) 的开头，继续 Reasoning）
  }
}
```

### 1.4 用伪代码理解 ReAct 循环

把源码简化成最容易理解的伪代码：

```python
# ReAct 伪代码（对应 ReactLoopAgent）
def react_loop(user_input):
    messages = [系统提示, 用户输入]

    while True:  # ← Agent Loop 的 while(true)
        # ══════ Reasoning 阶段 ══════
        response = call_llm(messages)  # 让 LLM 思考

        # ══════ 观察回复 ══════
        if response 没有工具调用:
            return response  # ← 最终回答，循环结束

        # ══════ Acting 阶段 ══════
        for tool_call in response.工具调用:
            result = execute_tool(tool_call)  # 执行工具
            messages.append(tool_call)        # 记录调用
            messages.append(result)           # 记录结果

        # ══════ 回到循环顶部，继续 Reasoning ══════
        # LLM 看到工具结果后，会重新推理下一步
```

### 1.5 一个具体的 ReAct 执行过程

```
用户："帮我查看北京天气并写一个报告"

═══ Turn 1, Step 1 ═══
[Reasoning] LLM 收到：系统提示 + 用户消息
            LLM 回复："我需要先查询天气"
            → 工具调用：weather(city="北京")

[Acting]    执行天气工具
            结果：晴天，25°C，湿度 60%

═══ Turn 1, Step 2 ═══
[Reasoning] LLM 收到：历史 + 工具结果
            LLM 回复："天气数据已获取，现在写报告"
            → 工具调用：write_file(path="report.md", content="...")

[Acting]    执行文件写入
            结果：文件创建成功

═══ Turn 1, Step 3 ═══
[Reasoning] LLM 收到：历史 + 工具结果
            LLM 回复："报告已创建完成，内容如下..."
            → 没有工具调用

[结束]      ReAct 循环结束
```

---

## 二、LLM 和 Agent 的边界

### 2.1 你的问题的本质

> "LLM 本身不具备联网功能，调用工具时是不是已经脱离了 LLM 的范畴？"

**不是脱离，而是 LLM 自己决定要调用工具**。

关键区别：

```
情况 A：你问 LLM "今天天气怎么样？"
  LLM：根据我的训练数据，天气是...（可能过时）

情况 B：你问 Agent "今天天气怎么样？"
  LLM：我需要调用天气工具查询实时数据
  → Agent 执行工具 → 结果返回给 LLM
  LLM：根据实时数据，今天北京晴天，25°C
```

**LLM 的角色没变**——它还是在"思考"和"回复"。变的是：

| 纯 LLM | Agent（LLM + 工具）|
|---|---|
| LLM 只能用自己的训练数据 | LLM 可以调用外部工具获取实时数据 |
| LLM 的回复是"编造"的 | LLM 的回复基于真实数据 |
| LLM 不能做事 | LLM 能指挥工具做事 |

> [!abstract] 边界在哪里
> **LLM 是大脑**——它决定"我需要什么信息"和"我需要做什么"。
>
> **工具是手脚**——它负责"去获取信息"和"去执行操作"。
>
> **Loop 是工作流程**——它负责"把大脑和手脚连接起来，反复迭代"。
>
> 调用工具不是"脱离 LLM"，而是**LLM 的能力延伸**。LLM 仍然是核心，工具只是让它能"做到"更多事。

### 2.2 从 LLM 到 Agent 的演进

```
Level 0: 纯 LLM
  "你好" → "你好！有什么可以帮你的？"
  一问一答，没有工具

Level 1: LLM + 单次工具调用
  "北京天气" → 调用天气工具 → "北京晴天 25°C"
  只调用一次工具，没有循环

Level 2: LLM + 工具 + 简单循环
  "帮我写一个脚本" → 调用写文件工具 → 检查结果 → 结束
  有循环但只执行一步

Level 3: Agent（LLM + 工具 + ReAct 循环）
  "帮我重构整个认证模块" → 分析 → 规划 → 分步执行 → 自我纠错 → 完成
  完整的 ReAct 循环，多步迭代

Level 4: Harness（Agent + 日志 + 插件 + 多 Agent + 安全）
  完整的工程化 Agent 系统
```

---

## 三、Session Log — 完整日志的详细解析

### 3.1 日志里具体包含什么

Session Log 是一个**有序的事件列表**，每个事件都有固定结构：

```typescript
{
  type: 'tool/call',        // 事件类型
  seq: 42,                  // 序号（第 42 条记录）
  time: 1725100000000,      // 时间戳
  data: {                   // 具体内容
    turn: 1,
    step: 1,
    callId: 'call_abc123',
    name: 'bash',
    arguments: '{"command": "ls"}'
  }
}
```

**完整的事件类型列表**：

| 事件类型 | 记录什么 | 谁产生 |
|---|---|---|
| `turn/start` | 一个轮次开始 | Agent Loop |
| `turn/end` | 一个轮次结束 + 原因 | Agent Loop |
| `step/start` | 一步开始（一次 LLM 调用）| Agent Loop |
| `step/end` | 一步结束 | Agent Loop |
| `user/message` | 用户输入或注入的上下文 | Agent Loop / 插件 |
| `assistant/chunk` | LLM 输出的**每个 token** | LLM 流式输出 |
| `assistant/message` | 组装后的完整助手消息 | Agent Loop |
| `tool/call` | 工具调用请求 | Agent Loop |
| `tool/result` | 工具执行结果 | 工具系统 |
| `request/header` | LLM 配置快照 | Agent Loop |
| `request/context` | 模型路由元数据 | Agent Loop |
| `todo/write` | 待办事项快照 | Todo 工具 |
| `session/end-seed` | 种子历史边界标记 | Session 构造函数 |

### 3.2 日志是给 AI 看的还是给人看的？

**两者都看，但目的不同**：

```
┌─────────────────────────────────────────────┐
│  Session Log                                 │
│                                             │
│  ┌─────────────────────┐                    │
│  │  AI 看的部分         │                    │
│  │                     │                    │
│  │  deriveMessages()   │ ← 从日志推导       │
│  │  输出：              │   LLM 需要的消息   │
│  │  [                 │   历史              │
│  │    {role:'system'},│                    │
│  │    {role:'user'},  │                    │
│  │    {role:'assistant'},│                  │
│  │    {role:'tool'}   │                    │
│  │  ]                 │                    │
│  └─────────────────────┘                    │
│                                             │
│  ┌─────────────────────┐                    │
│  │  人看的部分          │                    │
│  │                     │                    │
│  │  - 每一步做了什么     │ ← 调试、复盘      │
│  │  - 每个 token 的输出  │ ← 回放、分析      │
│  │  - 工具调用和结果     │ ← 排查问题        │
│  │  - 错误信息          │ ← 定位 bug        │
│  └─────────────────────┘                    │
└─────────────────────────────────────────────┘
```

**AI 看日志的方式**：不是直接看原始日志，而是通过 `deriveMessages()` 函数**推导**出 LLM 需要的消息格式。原始日志里有 `assistant/chunk`（逐 token），但 LLM 需要的是 `assistant/message`（完整消息）。

**人看日志的方式**：通过 UI 工具（如 Trajectory 视图）查看完整的事件流，可以回放、搜索、分析。

### 3.3 为什么需要保存日志

> [!tip] 类比：飞机黑匣子
> 黑匣子不是给飞行员实时看的，而是给**事故调查员**事后分析的。

Session Log 的核心价值：

| 用途 | 没有日志会怎样 | 有日志能做什么 |
|---|---|---|
| **恢复** | 程序崩溃后所有对话丢失 | 从断点继续（resume）|
| **回放** | 无法重现对话过程 | 精确回放每个 token |
| **调试** | 出了问题不知道哪一步出错 | 看日志定位问题 |
| **分析** | 不知道 Agent 的行为模式 | 分析 Agent 决策过程 |
| **分叉** | 无法从某个点重新开始 | fork 一个新会话从某步继续 |
| **合规** | 无法证明 Agent 做了什么 | 完整的操作审计记录 |

### 3.4 日志越来越大怎么办

这是个好问题。Harness 有几个机制控制日志膨胀：

#### 机制 1：Compaction（上下文压缩）

```
对话太长（接近上下文窗口限制）
  ↓
触发 Compaction
  ↓
把旧的对话历史压缩成摘要
  ↓
原始历史 → 压缩后的摘要（大幅减少 token 数）
  ↓
Session Log 本身不变，但 LLM 看到的消息变少了
```

#### 机制 2：Session 分割

长时间运行的任务可以分割成多个 Session，每个 Session 有独立的日志。

#### 机制 3：日志保留策略

```
旧日志的作用：
├── Resume：从之前的对话继续
├── Fork：从某个历史点分叉
├── Replay：重放对话分析行为
├── Audit：操作审计（合规需求）
└── Debug：排查历史问题
```

> [!abstract] 古早日志的价值
> 即使是很久以前的日志，也有价值：
> - **模式分析**：Agent 在类似任务上通常怎么做？
> - **错误复盘**：之前的 bug 是怎么出现的？
> - **知识积累**：Agent 从之前的对话中学到了什么？
> - **合规审计**：证明 Agent 没有做过危险操作
>
> 这就像公司的财务账本——即使是去年的账，也可能需要查。

---

## 四、架构层级关系

### 4.1 完整的层级图

```
┌─────────────────────────────────────────────────────────────┐
│  第五层：安全与协作                                           │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐                 │
│  │  Sandbox   │ │ Multi-    │ │  审批系统  │                 │
│  │ (安全沙箱)  │ │ Agent     │ │ (权限控制) │                 │
│  └───────────┘ └───────────┘ └───────────┘                 │
├─────────────────────────────────────────────────────────────┤
│  第四层：基础设施                                             │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐                 │
│  │ Session    │ │  Plugin   │ │  Preset   │                 │
│  │ Log (日志) │ │ System    │ │ (预设配置) │                 │
│  │           │ │ (插件化)   │ │           │                 │
│  └───────────┘ └───────────┘ └───────────┘                 │
├─────────────────────────────────────────────────────────────┤
│  第三层：核心循环                                             │
│  ┌─────────────────────────────────────────┐                │
│  │           Agent Loop (ReAct)            │                │
│  │     接收消息 → 调用 LLM → 执行工具 → 循环  │                │
│  └─────────────────────────────────────────┘                │
├─────────────────────────────────────────────────────────────┤
│  第二层：能力层                                               │
│  ┌───────────┐ ┌───────────┐                                │
│  │   Tools    │ │   LLM     │                                │
│  │ (工具系统)  │ │ (大语言模型)│                                │
│  └───────────┘ └───────────┘                                │
├─────────────────────────────────────────────────────────────┤
│  第一层：模型层                                               │
│  ┌─────────────────────────────────────────┐                │
│  │     LLM API（DeepSeek / OpenAI / ...）   │                │
│  └─────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 每一层的作用

| 层 | 组件 | 作用 | 类比 |
|---|---|---|---|
| **模型层** | LLM API | 提供语言理解和生成能力 | 大脑的生物学基础 |
| **能力层** | Tools + LLM 适配器 | 工具执行 + 模型调用 | 手脚 + 大脑 |
| **核心循环** | Agent Loop | ReAct 循环驱动 | 工作流程 |
| **基础设施** | Session Log / Plugin / Preset | 日志 / 可扩展 / 可配置 | 公司制度 |
| **安全与协作** | Sandbox / Multi-Agent / 审批 | 隔离 / 协作 / 权限控制 | 安保系统 |

### 4.3 组件之间的关系

```
LLM（大脑）
  │
  ├── 被 Agent Loop 调用（Loop 决定何时调用 LLM）
  │
  ├── 通过 LLM 适配器连接（适配器处理 API 差异）
  │
  └── 输出工具调用请求（LLM 生成 tool_call）

Tools（手脚）
  │
  ├── 被 Agent Loop 调用（Loop 决定何时执行工具）
  │
  ├── 在 Sandbox 中执行（沙箱隔离安全风险）
  │
  └── 结果返回给 Loop（Loop 把结果放回消息队列）

Agent Loop（工作流程）
  │
  ├── 驱动整个流程（while(true) 循环）
  │
  ├── 记录日志到 Session Log（每一步都写入）
  │
  ├── 通过 Plugin System 扩展（插件注入上下文、修改行为）
  │
  └── 管理 Multi-Agent（委派任务给子 Agent）
```

---

## 五、插件化在哪一层

### 5.1 答案：**每一层都可以插件化**

Cordis 的设计哲学是 **Everything is a Plugin**（一切皆插件）。在 Harness 里：

| 层 | 插件化的组件 | 源码位置 |
|---|---|---|
| **模型层** | LLM 适配器 | `packages/llm/llm-deepseek/` |
| **能力层** | 工具（bash、文件、搜索...）| `packages/core/tools/` |
| **核心循环** | Agent Loop 本身 | `packages/core/agent-loop/` |
| **基础设施** | Session 存储、Skill、Goal | `packages/session/`、`packages/skill/`、`packages/goal/` |
| **安全与协作** | Sandbox、审批、子 Agent | `packages/sandbox/`、`packages/interaction/`、`packages/subagent/` |

> [!warning] Agent Loop 可以插件化吗？
> **可以！** Agent Loop 本身就是一个 Cordis 插件。你可以换掉整个 Loop 实现，只要它遵守 `Agent` 接口。
>
> Harness 默认的 Loop 是 `ReactLoopAgent`，但你可以写一个完全不同的 Loop（比如不使用 ReAct 模式），然后通过插件系统替换它。

### 5.2 工具可以插件化吗

**可以，而且已经在这么做了。**

每个工具都是一个独立的插件：

```typescript
// 注册一个工具插件
ctx.tools.register('bash', {
  schema: { name: 'bash', description: '...', parameters: {...} },
  execute: async (args) => { ... }
})

// 换掉 bash 工具的实现
ctx.tools.register('bash', {
  schema: { name: 'bash', description: '...', parameters: {...} },
  execute: async (args) => { /* 完全不同的实现 */ }
})
```

### 5.3 插件化的层级关系

```
Cordis 微内核（Context）
  │
  ├── LLM 插件（替换模型）
  │     ├── llm-deepseek（DeepSeek 适配）
  │     ├── llm-openai（OpenAI 适配）
  │     └── llm-anthropic（Anthropic 适配）
  │
  ├── Tools 插件（替换工具）
  │     ├── tool-bash（Bash 工具）
  │     ├── tool-fs（文件工具）
  │     └── tool-web（搜索工具）
  │
  ├── Agent Loop 插件（替换循环）
  │     └── agent-loop（默认 ReAct 实现）
  │
  ├── Session 插件（替换存储）
  │     └── session（默认 JSONL 存储）
  │
  ├── Skill 插件（替换知识加载）
  │     └── skill-filesystem（从文件系统加载）
  │
  └── Goal 插件（替换目标追踪）
        └── goal（默认实现）
```

> [!abstract] 核心思想
> **没有不可替换的"核心"**。Cordis 的设计就是让每一层都可以被替换。你想换掉 LLM？换一个适配器插件。你想换掉工具系统？换一个工具注册表插件。你想换掉整个 Agent Loop？写一个新的 Loop 插件。
>
> 这就是 Harness 和其他 Agent 框架的最大区别——**真正的模块化**。

---

## 六、多 Agent — 实现与应用场景

### 6.1 多 Agent 是怎样实现的

```
主 Agent（项目经理）
  │
  ├─ [1] 决定委派任务
  │      使用 subagent 工具
  │
  ├─ [2] 创建子 Agent
  │      方式一：Fork — 克隆当前会话
  │      方式二：Spawn — 创建全新会话
  │      方式三：ACP — 委托给外部系统
  │
  ├─ [3] 子 Agent 独立执行
  │      有自己的 Agent Loop
  │      有自己的 Session Log
  │      有自己的工具集
  │
  ├─ [4] 子 Agent 完成
  │      通过 tool-subagent-report 返回结果
  │
  └─ [5] 主 Agent 继续
         整合所有子 Agent 的结果
```

**源码位置**：`packages/subagent/`（14 个子包）

### 6.2 应用场景

| 场景 | 怎么用多 Agent |
|---|---|
| **大型项目重构** | 主 Agent 分析 → Fork 多个子 Agent 并行重构不同模块 |
| **代码审查** | 主 Agent 写代码 → Spawn 审查 Agent 检查代码质量 |
| **测试生成** | 主 Agent 实现功能 → Spawn 测试 Agent 自动生成测试 |
| **文档生成** | 主 Agent 写代码 → Spawn 文档 Agent 生成 API 文档 |
| **部署流水线** | 主 Agent 触发 → 子 Agent 1 跑测试 → 子 Agent 2 部署 |

### 6.3 前端是否显示多 Agent

**是的**，Harness 的 Web UI 会显示：

```
┌──────────────────────────────────────┐
│  主 Agent: 重构认证模块                │
│                                      │
│  ├─ 子 Agent 1: 重构 login.py        │
│  │   状态: ✅ 完成                     │
│  │   耗时: 2 分钟                      │
│  │                                    │
│  ├─ 子 Agent 2: 重构 auth.py         │
│  │   状态: 🔄 执行中                   │
│  │   当前: 正在修改第 3 个函数           │
│  │                                    │
│  └─ 子 Agent 3: 写测试               │
│      状态: ⏳ 等待中                   │
│      (等子 Agent 1 和 2 完成)          │
└──────────────────────────────────────┘
```

子 Agent 的状态通过 Session Log 的 `origin: 'subagent'` 和 `delegationDepth` 字段追踪。

---

## 七、安全规范设计在哪一层

### 7.1 答案：**在 Harness 层，不是 LLM 层**

LLM 本身**没有安全机制**——它只是一个语言模型，输出文本。安全全靠 Harness 包装：

```
用户请求
  │
  ├─ LLM 层：没有任何安全检查
  │  （LLM 只是生成文本，不知道什么是"危险"）
  │
  └─ Harness 层：多重安全防线
     │
     ├─ [1] 权限预设（workspace-write / danger-full-access）
     │
     ├─ [2] Sandbox（隔离执行环境）
     │
     ├─ [3] 审批系统（危险操作需人类确认）
     │
     ├─ [4] 策略检查（文件/网络/进程策略）
     │
     └─ [5] 超时控制（防止执行卡死）
```

### 7.2 为什么安全不在 LLM 层

LLM 无法做安全检查，因为：

1. **LLM 不理解"执行"**——它只是生成文本，不知道 `rm -rf /` 实际上会删除文件
2. **LLM 没有权限控制**——它不知道当前用户有什么权限
3. **LLM 无法隔离执行**——它只是输出文字，无法控制执行环境

安全必须由**包围 LLM 的 Harness**来实现。

---

## 八、流式 Token — 什么是"流式"

### 8.1 什么是流式

> [!tip] 类比：水龙头 vs 一桶水
>
> **非流式**（一桶水）：等 LLM 想好整句话，一次性给你
> ```
> 等待 5 秒...
> "今天北京天气晴朗，气温 25°C，适合外出。"
> ```
>
> **流式**（水龙头）：LLM 想一个字给你一个字
> ```
> 今 → 天 → 北 → 京 → 天 → 气 → 晴 → 朗 → ...
> ```

### 8.2 为什么每个 token 是一个事件

在 Harness 里，流式输出的每个 token 都被记录为一个独立的 `assistant/chunk` 事件：

```typescript
// agent.ts:347-351
const stream = this.loopCtx.llm.stream(request)
for await (const chunk of stream) {
  // 每个 chunk = 一个或几个 token
  this.session.append('assistant/chunk', { turn, step, chunk })
  assembler.push(chunk)
}
```

**为什么这样做？**

| 好处 | 解释 |
|---|---|
| **实时显示** | UI 可以逐字显示 LLM 的回复 |
| **完美回放** | 可以精确重现 LLM 的生成过程 |
| **断点恢复** | 程序崩溃后可以从最后一个 token 继续 |
| **Token 用量统计** | 每个 token 都被计数 |
| **延迟分析** | 可以分析 LLM 的生成速度 |

### 8.3 流式的过程

```
LLM 服务器                    Harness                      用户界面
   │                            │                            │
   │  ── chunk: "今" ────────▶  │  记录 assistant/chunk      │  显示 "今"
   │  ── chunk: "天" ────────▶  │  记录 assistant/chunk      │  显示 "今天"
   │  ── chunk: "北" ────────▶  │  记录 assistant/chunk      │  显示 "今天北"
   │  ── chunk: "京" ────────▶  │  记录 assistant/chunk      │  显示 "今天北京"
   │  ── chunk: "天" ────────▶  │  记录 assistant/chunk      │  显示 "今天北京天"
   │  ── chunk: "气" ────────▶  │  记录 assistant/chunk      │  显示 "今天北京天气"
   │  ...                       │  ...                       │  ...
   │  ── chunk: "" (结束) ────▶ │  组装 assistant/message    │  显示完成
```

> [!note] 源码对应
> - `assistant/chunk` = 每个 token 一个事件（`agent.ts:349`）
> - `assistant/message` = 组装后的完整消息（`agent.ts:381`）
> - `assembler` = 把 chunk 拼成完整消息的工具

---

## 九、Goal 系统 — 有状态的任务追踪

### 9.1 Goal 是什么

> [!tip] 类比：项目管理工具上的任务卡片
>
> Goal = **一个有状态的任务卡片**：
>
> ```
> 任务：修复登录模块的 bug
> 状态：进行中
> 进度：已完成分析，正在修改代码
> 已执行轮次：3/10
> ```

### 9.2 Goal 的结构

```typescript
{
  objective: "修复登录模块的 bug",  // 目标描述
  phase: "active",                  // 状态
  revision: 3,                      // 版本号
  roundsStarted: 2,                 // 已执行轮次
  maxGoalRounds: 10                 // 最大轮次
}
```

### 9.3 Goal 的状态流转

```
创建 Goal
  │
  ├─ active（活跃）→ Agent 正在执行
  │   │
  │   ├─ complete（完成）→ 任务完成
  │   │
  │   ├─ paused（暂停）→ Agent 暂停
  │   │   └─ active → 恢复执行
  │   │
  │   └─ blocked（阻塞）→ 遇到无法解决的问题
  │
  └─ 达到 maxGoalRounds → 自动暂停
```

### 9.4 Goal Round Driver — 自动继续

这是 Goal 系统最巧妙的部分：

```
Agent 完成一步
  │
  ├─ Goal Round Driver 检查
  │  Goal 状态 = active？
  │  轮次 < maxGoalRounds？
  │
  ├─ 如果是 → 自动发送 continuation 消息
  │  "你的目标是修复登录 bug，请继续"
  │
  └─ Agent 收到消息 → 继续执行
     ...
     Goal 完成 → Driver 停止
```

**为什么需要这个？**

没有 Goal Round Driver：
```
用户："帮我重构整个认证模块"
Agent：（执行一步）"我已经修改了 login.py"
用户："继续"
Agent：（执行一步）"我已经修改了 auth.py"
用户："继续"
Agent：（执行一步）"我已经写了测试"
用户："继续"
...
```

有 Goal Round Driver：
```
用户："帮我重构整个认证模块"
Agent：（自动创建 Goal）
Agent：（自动执行多步，每步完成后自动继续）
Agent："认证模块重构完成，所有测试通过"
```

### 9.5 Goal 的工具

| 工具 | 作用 | 使用场景 |
|---|---|---|
| `get_goal` | 查看当前 Goal 状态 | Agent 想知道进度 |
| `create_goal` | 创建新 Goal | Agent 确定要执行的任务 |
| `update_goal` | 更新 Goal 状态 | Agent 完成/暂停/阻塞任务 |

> [!note] 源码位置
> - `packages/goal/goal/` — Goal 服务
> - `packages/goal/tool-goal/` — Goal 工具
> - `packages/goal/goal-round-driver/` — 自动继续驱动

---

## 小结

| 问题 | 答案 |
|---|---|
| ReAct 是什么 | 推理（Reasoning）+ 行动（Acting）交替循环 |
| ReAct 怎么实现的 | `while(true)` 循环：preStep → step → 检查是否继续 |
| LLM 和 Agent 的边界 | LLM 是大脑，Agent = LLM + 工具 + 循环。调用工具不是脱离 LLM，而是能力延伸 |
| Session Log 给谁看 | 两者都看。AI 通过 `deriveMessages()` 推导消息历史；人通过 UI 查看调试 |
| 日志越来越大怎么办 | Compaction 压缩 + Session 分割 + 保留策略 |
| 古早日志有什么用 | Resume / Fork / Replay / Audit / Debug |
| 架构层级 | 模型层 → 能力层 → 核心循环 → 基础设施 → 安全协作 |
| 插件化在哪一层 | **每一层都可以插件化**（Everything is a Plugin）|
| 多 Agent 怎么实现 | Fork / Spawn / ACP，每个子 Agent 有独立的 Loop 和 Log |
| 多 Agent 前端显示 | 是，UI 会显示子 Agent 的状态和进度 |
| 安全在哪一层 | Harness 层（Sandbox + 审批 + 策略），不是 LLM 层 |
| 流式是什么 | LLM 逐 token 输出，不是一次性返回 |
| 每个 token 为什么是事件 | 为了实时显示、完美回放、断点恢复、用量统计 |
| Goal 系统是什么 | 有状态的任务追踪 + 自动继续执行 |

---

## 相关笔记

- [[Harness 工程]] / [[上下文工程]] / [[Agent 评估]] —— 设计原理视角的Harness五要素、上下文与评估

- [[02-核心概念]] — Agent = LLM + Tools + Loop
- [[07-Agent Loop 深度拆解]] — ReactLoopAgent 源码详解
- [[08-工具系统]] — 工具注册和执行
- [[09-Session 日志]] — 日志系统详解
- [[11-子 Agent 与多 Agent]] — 多 Agent 协作
- [[13-Skill 与 Goal 系统]] — Goal 系统详解
- [[14-Sandbox 与安全]] — 安全机制详解
