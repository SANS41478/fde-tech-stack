---
title: TypeScript 速成 — 读懂 Harness 代码的最小知识
aliases:
  - TS 速成
  - TypeScript 基础
tags:
  - deepseek-harness
  - typescript
  - 编程语言
created: 2026-08-31
type: tutorial
domain: ai
layer: implementation
canonical: false
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://github.com/deepseek-ai/deepseek-harness]
---

# TypeScript 速成 — 读懂 Harness 代码的最小知识

> [!tip] 目标
> 只讲**读懂 DeepSeek Harness 源码**所需的最小 TypeScript 知识。不需要成为 TS 专家，只需要能看懂代码在做什么。

---

## 1. TypeScript 是什么

> [!tip] 类比
> JavaScript = 没有标签的快递（你知道里面是东西，但不知道是什么）
>
> TypeScript = 贴了标签的快递（标签写着"易碎品-玻璃杯"）

TypeScript = JavaScript + **类型标签**

它在 JavaScript 的基础上加了一层"类型检查"，让你在**运行之前**就能发现错误。

> [!note] Harness 为什么用 TypeScript
> Harness 是一个大型项目（54 个包），类型系统帮助开发者在写代码时就发现错误，而不是等运行时才报错。

---

## 2. 最常用的类型语法

### 2.1 基本类型

```typescript
// 文字（字符串）
let 名字: string = "小明"

// 数字
let 年龄: number = 25

// 布尔值（是/否）
let is_学生: boolean = true

// 任意类型（不想检查）
let 什么都可以: any = "可以是文字"
什么都可以 = 123  // 也行
```

> [!tip] 看代码时
> 当你看到 `let x: Type = value`，只需要知道：x 是一个变量，Type 是它的标签，value 是它当前的值。

---

### 2.2 接口（Interface）— 描述一个东西的结构

```typescript
// 定义"一个人长什么样"
interface 人 {
  姓名: string      // 必须有文字类型的姓名
  年龄: number      // 必须有数字类型的年龄
  爱好?: string[]   // 可选的爱好（字符串数组）
}

// 使用
let 小明: 人 = {
  姓名: "小明",
  年龄: 25,
  // 爱好可以不写，因为是可选的
}

let 小红: 人 = {
  姓名: "小红",
  年龄: 23,
  爱好: ["跑步", "读书"]  // 写了也行
}
```

> [!tip] 类比
> 接口就像**表格模板**：定义了表格应该有哪些列，每一列应该填什么类型的数据。

> [!note] Harness 里的例子
> `packages/core/session/src/types.ts` 里定义了 `SessionEventMap`，描述了每种事件的结构。当你看到 `turn/start: { turn: number }`，意思是"turn/start 事件有一个 turn 字段，类型是数字"。

---

### 2.3 泛型（Generic）— 通用模具

```typescript
// 没有泛型：每种类型要写一个函数
function 打印文字(x: string) { console.log(x) }
function 打印数字(x: number) { console.log(x) }

// 有泛型：一个函数适用所有类型
function 打印<T>(x: T) { console.log(x) }

// 使用
打印<string>("你好")   // T 被替换为 string
打印<number>(123)      // T 被替换为 number
打印<人>(小明)          // T 被替换为 人 类型
```

> [!tip] 类比
> 泛型就像**通用模具**：模具的形状（T）在使用时才确定。做饼干时模具是饼干形状，做巧克力时是巧克力形状。

> [!note] Harness 里的例子
> `SessionEvent<T extends SessionEventType = SessionEventType>` — T 是事件类型参数，使用时被替换为具体的事件类型。

---

### 2.4 联合类型（Union）— 多选一

```typescript
// 这个变量只能是这两个值之一
type 方向 = "上" | "下" | "左" | "右"

let 我的方向: 方向 = "上"   // 可以
let 错误: 方向 = "斜"       // 报错！"斜"不在选项里
```

> [!tip] 类比
> 联合类型就像**下拉菜单**：只能从预设的选项中选一个。

> [!note] Harness 里的例子
> `TurnEndReason` 是一个联合类型：`completed | aborted | blocked | error | max-tokens | interrupted`。每个值描述了"轮次为什么结束"。

---

### 2.5 async/await — 等待异步操作

```typescript
// 异步函数：发出请求后不阻塞
async function 查天气(城市: string): Promise<天气> {
  // await = "等这个完成后，再往下走"
  let 结果 = await fetch(`https://weather.com/${城市}`)
  let 天气 = await 结果.json()
  return 天气
}

// 使用
let 北京天气 = await 查天气("北京")
console.log(北京天气)
```

> [!tip] 类比
> `await` = 在餐厅点了菜后**等菜上来**再吃。你不会在菜还没上的时候就吃盘子。

> [!note] Harness 里的例子
> Agent Loop 里的 `turn()` 和 `step()` 都是 async 函数，因为调用 LLM 和执行工具都需要等待。

---

### 2.6 类型断言 — 告诉编译器"我知道这是什么"

```typescript
let 结果: any = 获取某个值()

// 告诉编译器：我知道这个值一定是 string 类型
let 文字: string = 结果 as string
```

> [!warning] 小心使用
> 类型断言就像**跟老师说"我知道答案"**——如果你真的知道，没问题；如果你不知道，运行时会出错。

---

## 3. 看 Harness 代码时最常见的语法

### 3.1 导入（import）— 从其他文件拿来用

```typescript
// 从 @deepseek-ai/dsh-session 包导入 Session 和 SessionId
import type { Session, SessionId } from '@deepseek-ai/dsh-session'

// 从本地文件导入
import { executeToolCalls } from './tool-calls.ts'
```

> [!tip] 理解方式
> `import` = "我需要别人写好的东西，从那个文件/包里拿过来用"

---

### 3.2 导出（export）— 让别人能用我的东西

```typescript
// 导出一个函数，其他文件可以 import 它
export async function executeToolCalls(...) { ... }

// 导出一个类型
export type InboxTarget = 'next-turn' | 'next-step'
```

> [!tip] 理解方式
> `export` = "我把这个东西放到台面上，谁需要谁可以拿"

---

### 3.3 类（Class）— 创建对象的模板

```typescript
// 定义一个"汽车"模板
class 汽车 {
  颜色: string
  速度: number

  constructor(颜色: string) {
    this.颜色 = 颜色
    this.速度 = 0
  }

  加速() {
    this.速度 += 10
  }

  刹车() {
    this.速度 = 0
  }
}

// 使用
let 我的车 = new 汽车("红色")
我的车.加速()
console.log(我的车.速度)  // 10
```

> [!tip] 类比
> 类 = 汽车工厂的**设计图纸**
>
> 对象 = 根据图纸造出来的**具体汽车**

> [!note] Harness 里的例子
> `ReactLoopAgent` 是一个类，它定义了 Agent Loop 的行为。每个 Agent 实例都是根据这个类创建的对象。

---

### 3.4 接口实现（implements）— 遵守合同

```typescript
// 定义一个合同：会飞的东西
interface 会飞 {
  飞(): void
}

// 鸟遵守这个合同
class 鸟 implements 会飞 {
  飞() {
    console.log("鸟在飞")
  }
}

// 飞机也遵守这个合同
class 飞机 implements 会飞 {
  飞() {
    console.log("飞机在飞")
  }
}
```

> [!note] Harness 里的例子
> `ReactLoopAgent implements Agent` — ReactLoopAgent 类遵守 Agent 接口定义的合同。

---

### 3.5 事件发射器（emit/on）— 广播消息

```typescript
// 定义一个事件系统
let 事件总线 = new EventEmitter()

// 监听事件
事件总线.on('着火', () => {
  console.log("收到着火事件，快跑！")
})

// 触发事件
事件总线.emit('着火')
// 控制台输出：收到着火事件，快跑！
```

> [!tip] 类比
> 事件 = 校园广播："全体师生请注意，现在发布通知"
>
> 监听 = 你打开收音机听广播
>
> 触发 = 广播站按下播放键

> [!note] Harness 里的例子
> Session Event 系统：`session.append('tool/call', data)` = 触发工具调用事件，所有监听者都会收到。

---

## 4. 读懂一段 Harness 代码的例子

让我们看一段真实的 Harness 代码（简化版）：

```typescript
// 从其他文件导入需要的东西
import type { Agent, AgentStatus } from '@deepseek-ai/dsh-agent'
import type { Session, SessionId } from '@deepseek-ai/dsh-session'

// 定义一个类，实现 Agent 接口
export class ReactLoopAgent implements Agent {
  // 属性：每个 Agent 实例都有的数据
  readonly id: SessionId          // 只读的会话 ID
  readonly inbox: Inbox           // 消息收件箱
  private phase: Phase            // 当前状态（私有，外部不能直接改）

  // 构造函数：创建 Agent 时调用
  constructor(
    private loopCtx: Context,     // 上下文（私有属性）
    public readonly id: SessionId,
    public readonly options: AgentOptions,
    public readonly session: Session,
  ) {
    // 初始化
    this.inbox = new Inbox(session, { ... })
    this.phase = { kind: 'idle', lastTurn: 0 }
  }

  // 方法：获取当前状态
  get status(): AgentStatus {
    return this.phase.kind === 'idle' ? 'idle' : 'running'
  }

  // 方法：发送消息
  send(message: UserMessage, target: InboxTarget, wakeup: boolean): void {
    this.inbox.splice(target, Infinity, 0, [message])
    if (wakeup) this.wakeDriver()
  }
}
```

**逐行解读**：

| 代码 | 含义 |
|---|---|
| `import type { ... }` | 从其他文件导入类型定义 |
| `export class ReactLoopAgent` | 导出一个叫 ReactLoopAgent 的类 |
| `implements Agent` | 这个类遵守 Agent 接口的合同 |
| `readonly id` | 每个实例有一个不能修改的 id |
| `private phase` | 私有属性，外部不能直接访问 |
| `constructor(...)` | 创建实例时的初始化代码 |
| `get status()` | getter 方法，读取状态 |
| `send(...)` | 发送消息的方法 |

---

## 5. 不需要深入的部分

作为初学者，以下内容你**不需要现在掌握**：

- [ ] 装饰器（Decorators）
- [ ] 命名空间（Namespaces）
- [ ] 高级泛型约束
- [ ] 映射类型（Mapped Types）
- [ ] 条件类型（Conditional Types）
- [ ] 模块解析细节

> [!tip] 策略
> 遇到看不懂的语法时：
> 1. 先看**函数名**和**变量名**猜测作用
> 2. 看**注释**（如果有的话）
> 3. 实在不懂就跳过，后面用到时再回来查

---

## 小结

| 语法 | 一句话解释 | 类比 |
|---|---|---|
| `let x: Type` | 给变量贴类型标签 | 快递标签 |
| `interface` | 定义数据的结构 | 表格模板 |
| `<T>` | 泛型，使用时才确定类型 | 通用模具 |
| `"a" \| "b"` | 联合类型，多选一 | 下拉菜单 |
| `async/await` | 等待异步操作 | 等菜上来 |
| `import/export` | 文件间共享代码 | 拿别人的东西/放东西到台面 |
| `class` | 创建对象的模板 | 工厂设计图纸 |
| `implements` | 遵守接口合同 | 签合同 |
| `emit/on` | 事件广播和监听 | 校园广播 |

---

## 下一步

了解了 TypeScript 基础后，我们来看看它运行的环境：[[05-Node.js 与 npm 速成]]。
