---
title: Node.js
aliases: [Nodejs, node, Node JS, JS 运行时]
tags: [fde, backend, javascript, runtime]
created: 2026-08-24
type: reference
domain: backend
layer: foundation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# Node.js

> [!abstract] 定位
> **Node.js** 是 JavaScript 的服务端运行时。当你的项目已经用 [[TypeScript]] / [[React]] / [[Next.js]] 写前端，用 Node 写轻量后端可以 **复用同一套语言与类型**，减少上下文切换。

---

> [!note] 重要澄清：Node.js 是「运行时」，不是「后端框架」
> 常有人把 Node.js 和 Django/FastAPI 并列叫「后端框架」——这是错的。Node.js 是 **JavaScript 的服务端运行时**（类比 Python 解释器），它让 JS 能跑在服务器上；真正写服务要用其上的**框架**（Express / Fastify / NestJS）。三者的层次区分见 [[后端基础]] 的「三者不是一回事」，以及 [[REST API]] 的设计风格定位。

## 一、Node 适合 FDE 的场景

- **轻量 API / [[Webhook]] 接收端**：处理第三方回调、转发事件。
- **BFF（Backend for Frontend）**：为前端组装数据，藏在 [[Next.js]] 背后。
- **SDK / 脚本**：很多 SaaS（见 [[SaaS 集成]]）官方 SDK 是 Node 版。
- **实时服务**：WebSocket、SSE 推送（配合 [[LLM API]] 流式）。

> [!note] 与 [[FastAPI]] 的分工
> AI 重逻辑（模型调用、向量检索、[[Agent]]）优先 Python；纯 Web 胶水、事件转发、前端同构，优先 Node。两者用 [[REST API]] 或 [[MCP]] 连接。

---

## 二、FDE 常用栈

```text
Node.js
├── Express / Hono / Fastify   # Web 框架
├── axios / node-fetch         # HTTP 客户端
├── ws / socket.io             # 实时
└── TypeScript                 # 类型保护
```

### 最小示例（Express + TS）
```ts
import express from "express";
const app = express();
app.use(express.json());

app.post("/webhook", (req, res) => {
  console.log(req.body);   // 第三方事件
  res.sendStatus(200);
});

app.listen(3000);
```

---

## 三、异步模型要点

Node 是 **单线程事件循环**，靠非阻塞 I/O 并发：
- 用 `async/await` 处理 Promise。
- 别写 CPU 密集同步循环，会阻塞整个进程。
- 高并发 I/O（如并发调 API）天然高效。

> [!tip] 和 Python asyncio 类比
> Node 的事件循环 ≈ Python 的 `asyncio` 事件循环；都是「等 I/O 时不闲着」。

---

## 四、常见坑

> [!warning]
> - **回调地狱 / 忘了 await**：Promise 不 await 拿不到结果。
> - **`module` vs `require` 混淆**：TS + ESM 时注意 `package.json` 的 `"type": "module"`。
> - **依赖体积爆炸**：`npm install` 拉一堆传递依赖，交付时配合锁定文件与 [[Docker]]。
> - **密钥进前端包**：Node 服务端才安全持有 [[OAuth]] / [[JWT]] 密钥。

---

相关笔记：
- [[TypeScript]] —— Node 的现代写法
- [[FastAPI]] —— Python 后端对照
- [[Webhook]] —— Node 常见用途
- [[REST API]] —— 接口设计
