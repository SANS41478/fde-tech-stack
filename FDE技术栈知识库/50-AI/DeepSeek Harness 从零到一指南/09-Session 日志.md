---
title: Session 日志 — Append-Only 事件流
aliases:
  - 会话日志
  - 事件日志
tags:
  - deepseek-harness
  - session
  - 日志
created: 2026-08-31
---

# Session 日志 — Append-Only 事件流

> [!tip] 目标
> 理解 Harness 的"记忆基石"——Session Log。它是所有组件的单一事实来源。

---

## 1. 为什么需要 Session Log

> [!tip] 类比：飞行记录仪
> Session Log 就像飞机上的**黑匣子**（飞行记录仪）：
>
> - 记录飞行中的**每一个操作**（飞行员按了什么按钮）
> - 记录**每一段对话**（飞行员和塔台说了什么）
> - 记录**每一个仪表读数**（速度、高度、航向）
>
> 飞机出了事故？看黑匣子回放就知道发生了什么。
>
> Agent 出了问题？看 Session Log 回放就知道哪一步出错。

**没有 Session Log**：
- Agent 做了什么？不知道
- 为什么做了错误决定？不知道
- 程序崩溃了？所有对话丢失

**有 Session Log**：
- 每一步都有记录
- 可以完整回放
- 可以从断点恢复
- 可以分析行为模式

---

## 2. Append-Only — 只能追加，不能修改

> [!tip] 类比：账本
> Session Log 就像一本**只能往后面写、不能涂改**的账本：
>
> - 3月1日：收入 100 元 ✅
> - 3月2日：支出 50 元 ✅
> - 3月1日：改成收入 200 元 ❌（不能修改！）
>
> 如果记错了怎么办？**再记一笔**：
> - 3月3日：更正：3月1日应为收入 200 元

这种设计的好处：
1. **不可篡改**：历史记录无法被修改
2. **完整回放**：可以从头到尾重放所有事件
3. **并发安全**：多个进程可以同时追加，不会冲突

---

## 3. 事件的结构

每个事件都有固定的结构：

```typescript
{
  type: 'tool/call',           // 事件类型
  seq: 42,                     // 序号（单调递增）
  time: 1725100000000,         // 时间戳（Unix 毫秒）
  data: {                      // 事件数据（根据 type 不同而不同）
    turn: 1,
    step: 1,
    callId: 'call_abc123',
    name: 'bash',
    arguments: '{"command": "ls"}'
  }
}
```

| 字段 | 含义 | 类比 |
|---|---|---|
| `type` | 这是什么事件 | 账本上的"收入"或"支出" |
| `seq` | 第几条记录 | 账本上的行号 |
| `time` | 什么时候发生的 | 账本上的日期 |
| `data` | 具体内容 | 账本上的金额和说明 |

---

## 4. 核心事件类型

### Turn 事件 — 轮次边界

```
turn/start { turn: 1 }     ← 第 1 轮开始
  ...                        ← 这一轮内的所有事件
turn/end { turn: 1, reason: 'completed' }  ← 第 1 轮结束
```

### Step 事件 — 步骤边界

```
step/start { turn: 1, step: 1 }   ← 第 1 轮第 1 步开始
  ...                               ← 这一步内的所有事件
step/end { turn: 1, step: 1 }     ← 第 1 轮第 1 步结束
```

### 消息事件 — 模型看到的内容

```
user/message {
  content: "帮我查看天气"
}                                  ← 用户消息

assistant/chunk {
  turn: 1, step: 1,
  chunk: { type: 'text', text: '我' }
}                                  ← LLM 输出的每个 token

assistant/message {
  turn: 1, step: 1,
  message: { content: [{ type: 'text', text: '我需要使用天气工具' }] }
}                                  ← 完整的助手回复

tool/call {
  turn: 1, step: 1,
  callId: 'call_abc',
  name: 'weather',
  arguments: '{"city": "北京"}'
}                                  ← 工具调用请求

tool/result {
  turn: 1, step: 1,
  message: { content: [{ type: 'text', text: '晴天，25°C' }] }
}                                  ← 工具执行结果
```

### 请求事件 — LLM 配置

```
request/header {
  header: {
    config: { provider: 'deepseek', model: 'deepseek-chat' },
    system: '你是一个助手...',
    tools: [...]
  },
  reason: 'initial'  // initial | resume | change
}
```

---

## 5. 核心不变量：Model-visible ⟺ logged

> [!abstract] 最重要的设计原则
> **模型看到的每一样东西，都必须记录在日志里。**
>
> 反过来说：**日志里没有的东西，模型不可能看到。**

这意味着：
- 每次 LLM 调用的输入（系统提示 + 历史 + 工具列表）→ 必须能从日志重建
- 每次 LLM 的输出 → 已记录（assistant/chunk + assistant/message）
- 每个工具调用和结果 → 已记录（tool/call + tool/result）

**为什么这很重要？**

```
如果模型看到了 X，但日志里没有记录 X
  → 程序崩溃后无法恢复（因为无法重建 X）
  → 无法回放对话（因为缺少 X）
  → 无法调试（因为不知道 X 是什么）
```

---

## 6. 从日志重建消息历史

LLM 需要的"对话历史"不是直接存储的，而是**从日志推导**出来的：

```
Session Log 中的事件：
  turn/start → user/message → assistant/message → tool/call → tool/result → ...

      ↓ 推导（deriveMessages）

LLM 看到的消息列表：
  [
    { role: 'system', content: '...' },
    { role: 'user', content: '帮我查看天气' },
    { role: 'assistant', content: '我需要使用天气工具' },
    { role: 'tool', content: '晴天，25°C' }
  ]
```

> [!note] 源码位置
> `packages/core/session/src/` — `deriveMessages()` 函数负责从日志推导消息历史

---

## 7. Surface — 有序消息面

Session Log 有一个**Surface**（表面）概念，是消息的有序视图：

```
Session Log（完整事件流）：
  turn/start → user/message → assistant/chunk → assistant/message → tool/call → tool/result → ...

      ↓ Surface（有序消息面）

Surface（只保留产生消息的事件）：
  user/message → assistant/message → tool/result → ...
```

**Surface 操作**：

| 操作 | 含义 | 用途 |
|---|---|---|
| `append` | 添加到末尾 | 正常的消息追加 |
| `replace` | 替换一段消息 | 上下文压缩（compaction） |

---

## 8. 事件的可忽略性（ignorable）

有些事件是**必须读取**的，有些是**可以跳过**的：

```typescript
{
  type: 'assistant/chunk',
  ignorable: true  // ← 标记为可忽略
}
```

| ignorable | 含义 | 如果遇到不认识的 type |
|---|---|---|
| `true` | 纯信息记录，不影响重建 | 可以安全跳过 |
| `false`（默认）| 影响对话重建 | 必须拒绝加载 |

> [!warning] 安全原则
> 遇到不认识的**必需事件**时，Harness 会**拒绝加载**整个会话，而不是静默跳过。这防止了数据损坏。

---

## 9. Session Format Version

日志格式有版本号，确保兼容性：

```typescript
export const SESSION_FORMAT_VERSION = 0  // 当前版本
```

**版本管理规则**：
- 版本号是**单调递增的整数**
- 旧版本的 Harness 拒绝加载新版本的日志
- 只有**结构性变化**才需要升版（事件结构、核心语义变化）
- 添加新的事件类型**不需要升版**（用 ignorable 标记）

---

## 10. 从日志恢复

当 Harness 重启或崩溃恢复时：

```
启动
  │
  ├─ [1] 加载存储的 Session Log
  │
  ├─ [2] 检查 SESSION_FORMAT_VERSION
  │      版本不匹配 → 拒绝加载
  │
  ├─ [3] 重放日志
  │      重建所有状态
  │      找到最后一个 turn/end 事件
  │
  ├─ [4] 检查是否有未完成的 turn
  │      有 → 标记为 'interrupted'
  │      无 → 正常启动
  │
  └─ [5] Agent Loop 从断点继续
         从 Inbox 取新消息
         开始新的 turn
```

---

## 11. 日志的实际样子

一段真实的 Session Log（简化）：

```json
[
  {
    "type": "turn/start",
    "seq": 1,
    "time": 1725100000000,
    "data": { "turn": 1 }
  },
  {
    "type": "user/message",
    "seq": 2,
    "time": 1725100000100,
    "data": { "content": "帮我写一个 hello world" },
    "surfaceOp": "append"
  },
  {
    "type": "step/start",
    "seq": 3,
    "time": 1725100000200,
    "data": { "turn": 1, "step": 1 }
  },
  {
    "type": "request/header",
    "seq": 4,
    "time": 1725100000300,
    "data": {
      "header": {
        "config": { "provider": "deepseek", "model": "deepseek-chat" },
        "system": "你是一个编程助手..."
      },
      "reason": "initial"
    }
  },
  {
    "type": "assistant/chunk",
    "seq": 5,
    "time": 1725100001000,
    "data": { "turn": 1, "step": 1, "chunk": { "type": "text", "text": "我" } }
  },
  {
    "type": "assistant/chunk",
    "seq": 6,
    "time": 1725100001100,
    "data": { "turn": 1, "step": 1, "chunk": { "type": "text", "text": "需要" } }
  },
  ...
]
```

---

## 小结

| 概念 | 一句话解释 |
|---|---|
| Session Log | Agent 的黑匣子，记录一切 |
| Append-Only | 只能追加，不能修改 |
| 事件结构 | type + seq + time + data |
| Surface | 有序消息面，只保留产生消息的事件 |
| ignorable | 可选事件，遇到不认识的可以跳过 |
| Format Version | 日志格式版本，确保兼容性 |
| deriveMessages | 从日志推导 LLM 需要的消息历史 |

---

## 下一步

理解了日志系统后，我们来看看 Harness 如何管理记忆：[[10-记忆与上下文]]。
