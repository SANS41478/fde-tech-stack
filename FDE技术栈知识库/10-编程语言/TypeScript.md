---
title: TypeScript
aliases: [TypeScript, JavaScript, TS, JS, 前端语言]
tags: [fde, language, frontend]
created: 2026-08-24
type: reference
domain: language
layer: foundation
canonical: true
canonical_group: language-typescript
status: active
updated: 2026-09-15
sources: []
---

# TypeScript

> [!abstract] 定位
> **TypeScript / JavaScript 是 FDE 的第二优先级语言**。当场景是 Web 应用、前端 Demo、Node 服务、SDK 或 AI 应用界面时，TS 比 Python 更顺手。

---

## 一、TypeScript 与 JavaScript 的关系

- **JavaScript** 是浏览器原生语言，无需编译。
- **TypeScript** 是 JS 的超集，加了 **静态类型**，能在写代码时就发现错误。

> [!tip] FDE 该用哪个
> 几乎总是用 **TypeScript**。类型系统在和 [[LLM API]] 返回结构、[[Structured Output]] 对接时，能显著减少「字段拼错」类 bug。纯 JS 只在写一次性小脚本时考虑。

---

## 二、TypeScript 主要用在哪

- **Web 应用**：搭配 [[React]] / [[Next.js]]
- **前端 Demo**：让客户看到可交互界面
- **Node.js 服务**：轻量后端或 [[Webhook]] 接收端
- **SDK / 客户端**：很多 SaaS（见 [[SaaS 集成]]）官方 SDK 是 TS
- **AI 应用界面**：聊天 UI、仪表盘

推荐技术树：
```text
TypeScript
├── React          # UI 组件
├── Next.js       # 全栈框架
├── Node.js       # 运行时
└── Tailwind CSS  # 样式
```

---

## 三、FDE 需要掌握的 TS 要点

### 1. 类型即文档
```ts
interface Ticket {
  category: string;
  priority: number;
  createdAt: Date;
}
```
和后端 Pydantic 模型对应，前后端契约一致。

### 2. 异步与 Promise
```ts
const res = await fetch("/api/tickets");
const data: Ticket[] = await res.json();
```
> 注意和 [[REST API]] 的状态码、错误处理配合。

### 3. 前端框架集成
- [[React]] 的 `useState` / `useEffect` 管理状态与副作用。
- [[Next.js]] 的 API Route 可直接写后端逻辑，省去单独起服务。

---

## 四、Python vs TypeScript：FDE 怎么选

| 场景 | 选 Python | 选 TypeScript |
| --- | --- | --- |
| 调模型 + 数据处理 | ✅ |  |
| AI 后端服务 | ✅（[[FastAPI]]） | ✅（Node） |
| 客户可见的 Web UI |  | ✅ |
| 浏览器端逻辑 |  | ✅ |
| 快速脚本 | ✅ |  |

> [!note] 现实组合
> 多数 FDE 项目是 **TS 做前端 + Python 做 AI 后端**，中间用 [[REST API]] 或 [[MCP]] 连接。

---

## 五、常见坑

> [!warning]
> - **`any` 滥用**：等于放弃类型保护，宁可显式定义接口。
> - **忘记 `await`**：异步函数不 await，拿到的是 Promise 而非数据。
> - **CORS 问题**：前端调后端跨域，需在后端（[[FastAPI]]）配置 CORS，或用 [[Next.js]] 的同域 API Route 规避。

---

相关笔记：
- [[Python]] —— 第一优先级语言
- [[React]] / [[Next.js]] —— TS 的主战场
- [[FDE 学习路线]] —— TS 在第二阶段
