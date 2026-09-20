---
title: Cordis 插件系统 — Harness 的骨架
aliases:
  - 微内核
  - 插件架构
tags:
  - deepseek-harness
  - cordis
  - 插件系统
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

# Cordis 插件系统 — Harness 的骨架

> [!tip] 目标
> 理解 DeepSeek Harness 的底层骨架——Cordis 微内核插件系统。这是理解 Harness "为什么这样设计"的关键。

---

## 1. 为什么需要插件系统

> [!tip] 类比：手机操作系统
> 想象你造了一部手机：
>
> **没有插件系统**：所有功能都焊死在主板上
> - 想加新功能？拆了重造
> - 想换掉相机？不可能
> - 想升级系统？整个换掉
>
> **有插件系统**：所有功能都是可插拔的模块
> - 想加新功能？插一个新模块
> - 想换掉相机？拔掉旧的，插新的
> - 想升级系统？只换需要升级的模块

Cordis 就是 DeepSeek Harness 的"插件系统"——**一切皆插件**。

---

## 2. Cordis 的五个核心概念

### 2.1 插件（Plugin）— 可插拔的模块

> [!tip] 类比：乐高积木
> 每个插件就像一块乐高积木：
> - 有**固定的接口**（积木的凸起和凹槽）
> - 有**具体的功能**（这块是轮子，那块是窗户）
> - 可以**自由组合**（你想怎么拼就怎么拼）

在代码里，一个最简单的插件：

```typescript
// 一个最简单的插件：提供"问候"服务
function 问候插件(ctx: Context) {
  // 注册一个服务到上下文中
  ctx.问候 = {
    说你好: (名字) => `你好，${名字}！`
  }
}
```

> [!note] Harness 里的例子
> `packages/core/tools/` 是一个插件，提供工具注册和执行服务
>
> `packages/llm/llm/` 是一个插件，提供 LLM 调用服务
>
> `packages/core/session/` 是一个插件，提供会话日志服务

---

### 2.2 Context（上下文）— 存放所有插件的仓库

> [!tip] 类比：工具箱
> Context 就像一个**大工具箱**，里面放着所有插件提供的工具：
>
> ```
> ctx.tools      ← 工具注册表（来自 tools 插件）
> ctx.llm        ← LLM 调用器（来自 llm 插件）
> ctx.sessions   ← 会话存储（来自 session 插件）
> ctx.skills     ← 技能注册表（来自 skill 插件）
> ```
>
> 每个插件往工具箱里放自己的工具，其他插件从工具箱里取用。

---

### 2.3 依赖注入（Dependency Injection）— 我需要什么

> [!tip] 类比：餐厅后厨
> 依赖注入就像**餐厅后厨的协作**：
>
> 炒菜师傅说："我需要灶台和食材"
> → 等灶台和食材都准备好了，炒菜师傅才开始工作
>
> 在代码里：
> ```typescript
> function 炒菜插件(ctx: Context) {
>   // 声明：我需要灶台和食材
>   // 等这两个服务都注册了，这个插件才激活
>   // 然后开始炒菜
> }
> ```

> [!abstract] 技术定义
> 依赖注入是一种设计模式：组件声明自己需要什么服务，框架负责在服务可用时才激活组件。组件不需要知道服务从哪里来，只需要知道"我需要它"。

---

### 2.4 事件系统（Events）— 广播消息

> [!tip] 类比：校园广播
> 事件系统就像**校园广播**：
>
> **触发事件** = 广播站按下播放键："着火了！"
>
> **监听事件** = 所有人打开收音机听到了这个消息
>
> **处理事件** = 听到"着火了"的人开始跑

在 Harness 里有三种事件模式：

#### emit（触发）— 广播，谁爱听谁听

```typescript
// 触发一个事件
ctx.emit('tool/call', { name: 'bash', arguments: '...' })

// 监听这个事件（可以有多个监听者）
ctx.on('tool/call', (event) => {
  console.log('工具被调用了：', event.name)
})
```

#### waterfall（瀑布）— 传递接力棒，每个人可以修改

```typescript
// waterfall 模式：事件传递时，每个监听者可以修改内容
ctx.waterfall('agent/pre-step', { messages }, async (messages) => {
  // 在消息里注入额外上下文
  messages.push({ content: '额外信息' })
  return messages  // 传给下一个监听者
})
```

> [!tip] waterfall 类比
> 就像**传纸条**：
> A 写了一句话 → 传给 B → B 可以加内容 → 传给 C → C 可以再加 → 最终到达目的地

#### serial（串行）— 一个接一个执行

```typescript
// serial 模式：监听者按顺序执行，前一个完成才执行下一个
ctx.serial('agent/turn-stopping', async () => {
  // 在轮次结束前做清理工作
})
```

---

### 2.5 可逆效果（Reversible Effects）— 拆卸时自动拆除

> [!tip] 类比：临时建筑
> 可逆效果就像**搭建临时建筑**：
>
> 搭建时：`ctx.effect(() => { ... })` 返回一个"拆除函数"
>
> 拆除时：调用返回的函数，所有注册的东西自动卸载

```typescript
// 注册一个工具
const 取消注册 = ctx.effect(() => {
  ctx.tools.register('my-tool', { ... })
})

// 不需要这个工具了
取消注册()  // 工具自动从注册表中移除
```

> [!abstract] 技术定义
> 可逆效果确保插件卸载时，它注册的所有服务、事件监听、工具等都被自动清理，不会留下"垃圾"。

---

## 3. 一个完整的插件例子

```typescript
// 这是一个完整的 Cordis 插件
function 天气插件(ctx: Context) {
  // 声明依赖：我需要 LLM 服务
  // （等 ctx.llm 准备好了，这个插件才激活）

  // 效果 1：注册一个天气工具
  ctx.effect(() => {
    ctx.tools.register('weather', {
      name: 'weather',
      description: '查询指定城市的天气',
      parameters: {
        city: { type: 'string', description: '城市名称' }
      },
      execute: async (args) => {
        const 天气 = await 查询天气API(args.city)
        return { content: 天气 }
      }
    })
  })

  // 效果 2：监听 LLM 请求，在系统提示里加入天气信息
  ctx.effect(() => {
    ctx.on('agent/pre-step', async (event) => {
      // 在消息里注入今天的天气
      event.messages.push({
        content: '今天北京天气：晴，25°C'
      })
    })
  })
}
```

**这个插件做了两件事**：
1. 注册了一个 `weather` 工具，让 Agent 可以查询天气
2. 在每次 Agent 思考前，注入今天的天气信息

---

## 4. Harness 的插件树

DeepSeek Harness 启动时，会从配置文件加载一个**插件树**：

```
Cordis 根 Context
├── dsh-base（基础层）
│   ├── 模型适配器（llm-deepseek）
│   ├── 工具注册表（tools）
│   ├── 会话存储（session）
│   ├── 沙箱（sandbox-local）
│   ├── 审批系统（user-approval）
│   ├── 设置管理（settings）
│   └── 凭据管理（credentials）
│
├── dsh-web-app（Web 应用层）
│   ├── Web UI（web）
│   └── 浏览器工具（web-search, web-fetch）
│
└── 用户自定义层
    └── cordis.patch.yml（用户覆盖配置）
```

**层级应用顺序**：
1. 每个 bundle 按顺序加载
2. profile 的 patch 覆盖特定配置
3. home 级 patch 再覆盖
4. `--patch` 命令行参数最后覆盖

> [!note] 查看你的插件树
> ```bash
> dsh --profile web --dump-config
> ```
> 这会打印当前配置下的完整插件树。

---

## 5. Capability Seam（能力接缝）

> [!tip] 类比：USB 接口
> 每个能力都有一个**标准接口**（USB），你可以换掉实现但接口不变：
>
> - 想换键盘？拔掉旧的，插新的（接口一样）
> - 想换鼠标？拔掉旧的，插新的（接口一样）

Harness 的能力接缝有三个角色：

| 角色 | 作用 | 类比 |
|---|---|---|
| Service Definition | 定义接口 | USB 接口标准 |
| Service Provider | 实现接口 | 具体的键盘/鼠标 |
| Consumer | 使用接口 | 电脑（通过 USB 使用设备） |

比如文件系统能力接缝：

```
Service Definition: ctx.fs（文件系统接口）
    ↓
Service Provider: sandbox-local（本地沙箱实现）
    ↓
Consumer: bash 工具（通过 fs 读写文件）
```

**换掉 Provider 就能换掉整个能力**：

```
把 Provider 从 sandbox-local 换成 remote-sandbox
    ↓
所有通过 fs 的操作都自动变成远程操作
    ↓
bash、PTY、LSP 全部跟着走
```

---

## 6. Bundle 和 Profile

### Bundle — 分发格式

> [!tip] 类比：宜家家具的包装盒
> Bundle 就是**一个功能包的标准包装**：
> - 包含所有需要的零件（插件代码）
> - 包含组装说明（cordis.patch.yml）
> - 可以被其他包引用

### Profile — 产品配置

> [!tip] 类比：宜家的样板间
> Profile 就是**一个完整的配置方案**：
> - 列出需要哪些 Bundle（哪些家具）
> - 定义覆盖规则（用户自定义）
> - 保存用户的个性化设置

Harness 内置了两个 Profile：

| Profile | 内容 | 用途 |
|---|---|---|
| `web` | dsh-base + dsh-web-app | Web UI 模式 |
| `headless` | dsh-base + headless runner | 命令行一次性任务 |

---

## 7. 为什么 Cordis 这么重要

Cordis 不仅仅是一个插件框架，它定义了 Harness 的**整个设计哲学**：

| 设计原则 | 在 Harness 中的体现 |
|---|---|
| 一切皆插件 | 模型、工具、日志、循环本身都是插件 |
| 依赖注入 | 插件声明依赖，框架自动解决 |
| 事件驱动 | 插件通过事件通信，松耦合 |
| 可逆效果 | 插件卸载时自动清理 |
| 能力接缝 | 换掉一个 Provider 就能换掉整个能力 |
| 层叠配置 | 多层配置可以覆盖和定制 |

> [!abstract] 核心思想
> **没有特权核心**：Harness 没有一个"不能改"的核心。你通过挂载插件来扩展它，所有注册都是可逆的效果。
>
> 这意味着：你可以换掉模型适配器、换掉工具注册表、换掉 Agent Loop 本身——**一切都可以从配置替换**。

---

## 小结

| 概念 | 一句话解释 | 类比 |
|---|---|---|
| 插件 | 可插拔的功能模块 | 乐高积木 |
| Context | 存放所有插件的仓库 | 工具箱 |
| 依赖注入 | 声明需要什么，框架自动解决 | 后厨协作 |
| 事件系统 | 插件间的通信机制 | 校园广播 |
| 可逆效果 | 插件卸载时自动清理 | 临时建筑 |
| 能力接缝 | 标准化的接口，实现可替换 | USB 接口 |
| Bundle | 功能包的标准包装 | 宜家包装盒 |
| Profile | 完整的配置方案 | 宜家样板间 |

---

## 下一步

理解了插件系统后，我们来深入 Harness 最核心的部分：[[07-Agent Loop 深度拆解]]。
