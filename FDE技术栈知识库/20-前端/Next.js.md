---
title: Next.js
aliases: [Nextjs, next, Next JS, 全栈 React 框架]
tags: [fde, frontend, fullstack]
created: 2026-08-24
type: reference
domain: frontend
layer: foundation
canonical: true
canonical_group: frontend-nextjs
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://nextjs.org/docs]
---

# Next.js

> [!abstract] 定位
> **Next.js** 是建立在 [[React]] 之上的全栈框架。对 FDE 而言，它是「前端 Demo + 轻后端 + 一键部署」的一站式方案，极大缩短从想法到可演示系统的距离。

---

## 一、为什么 FDE 爱用 Next.js

```text
客户需求
   ↓
Next.js      ← 前端 UI（React）
   ↓
React UI
   ↓
FastAPI      ← 或 Next 自身 API Route 做后端
   ↓
数据库 / AI
```

优势：
- **一个项目同时有前端和后端**：API Route 可以直接写服务端逻辑，不必单独起 [[FastAPI]]（虽然复杂 AI 逻辑仍推荐 Python）。
- **文件路由**：`app/tickets/page.tsx` 自动变成 `/tickets`，省去路由配置。
- **SSR / SSG**：首屏快、SEO 友好。
- **部署简单**：Vercel / [[Docker]] 都能跑，配合 [[云平台]] 上线快。

> [!tip] FDE 黄金组合
> 简单项目：Next.js 前端 + Next API Route 后端。
> AI 重项目：Next.js 前端 + [[FastAPI]] 后端（AI 部分用 Python）。

---

## 二、FDE 常用能力

### 1. 页面（App Router）
```tsx
// app/page.tsx
export default function Home() {
  return <h1>客户 Demo</h1>;
}
```

### 2. API Route（服务端）
```tsx
// app/api/tickets/route.ts
export async function GET() {
  const data = await fetchTickets(); // 调 DB 或 LLM
  return Response.json(data);
}
```
> 这里可以安全地放 [[OAuth]] 密钥，不暴露给浏览器。

### 3. 服务端组件 vs 客户端组件
- 服务端组件：直接读 [[PostgreSQL]]，不进浏览器包。
- 客户端组件：需要交互（点击、输入）时加 `"use client"`。

### 4. 流式输出（AI Chat）
配合 [[LLM API]] 的 Streaming，用 `ReadableStream` 把 token 逐步推到前端，体验更像真产品。

---

## 三、和 AI 的契合点

- 聊天界面（AI Chat UI）天然适合 Next.js。
- 可在 API Route 里调用 [[LLM API]]、做 [[RAG]] 检索、返回 [[Structured Output]]。
- 配合 [[Tailwind CSS]] + shadcn/ui 快速出专业感界面。

---

## 四、常见坑

> [!warning]
> - **密钥放错地方**：`NEXT_PUBLIC_` 前缀的变量会进浏览器，绝不放密钥。
> - **API Route 变重**：AI 逻辑（模型调用、向量检索）塞进 Next 会让项目臃肿，复杂时拆到 [[FastAPI]]。
> - **不注意缓存**：Next 默认缓存 fetch，调实时数据要加 `cache: "no-store"`。

## 五、交付检查

- 服务端与客户端边界明确，敏感数据只在服务端处理。
- Loading、错误、空数据和权限不足状态都可被直接访问和测试。
- Server Action / API Route 有输入 Schema、认证、授权、限流和审计。
- 缓存策略写明失效条件，不能把租户数据或实时状态误缓存。
- 关键页面有移动端、键盘和 E2E 验收。

---

相关笔记：
- [[React]] —— Next 的 UI 基础
- [[Tailwind CSS]] —— 快速样式
- [[FastAPI]] —— 重 AI 后端的可选拆分
- [[UI UX、设计系统与动效]] —— 页面状态、设计系统和交互质量
- [[API 产品化]] —— API Route 的契约、校验和演进
- [[Web 用户认证与安全]] —— Middleware、Session 与 RBAC
- [[Web 测试与 E2E]] —— 关键页面与用户旅程验证
- [[Node.js 项目环境与本地运行]] —— 项目初始化、构建和 localhost
- [[FDE 学习路线]] —— 第二阶段核心
