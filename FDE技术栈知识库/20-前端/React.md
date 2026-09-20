---
title: React
aliases: [react, React.js, 组件化 UI]
tags: [fde, frontend, ui]
created: 2026-08-24
type: reference
domain: frontend
layer: foundation
canonical: true
canonical_group: frontend-react
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://react.dev/learn]
---

# React

> [!abstract] 定位
> **React** 是 FDE 做前端 Demo、管理后台、AI Chat UI、数据展示页的组件化基础。FDE 不必成为专业前端，但必须能用 React 快速拼出「客户能点的界面」。

---

## 一、React 解决了什么问题

传统页面是「一整页 HTML」。React 把它拆成 **可复用组件**，状态变化时只更新需要的部分。对 FDE 的价值是：

- **快速拼装**：把按钮、表单、列表做成组件，像搭积木。
- **状态驱动 UI**：数据变了，界面自动变，不用手动操作 DOM。
- **生态庞大**：[[Tailwind CSS]]、组件库（shadcn/ui）直接可用。

---

## 二、FDE 必须懂的核心概念

### 1. 组件（Component）
```tsx
function TicketCard({ ticket }: { ticket: Ticket }) {
  return <div className="p-4 border rounded">{ticket.category}</div>;
}
```

### 2. 状态（useState）
```tsx
const [tickets, setTickets] = useState<Ticket[]>([]);
```

### 3. 副作用（useEffect）
```tsx
useEffect(() => {
  fetch("/api/tickets").then(r => r.json()).then(setTickets);
}, []);
```
> 这里调的就是 [[REST API]] 的后端（常是 [[FastAPI]]）。

### 4. 受控表单
收集用户输入，发给后端或 [[LLM API]] 处理。

---

## 三、FDE 用 React 的典型页面

- **客户 Demo**：展示「这个功能真的能工作」
- **管理后台**：增删查改业务数据（[[PostgreSQL]]）
- **AI Chat UI**：问答界面，流式展示模型输出（[[LLM API]] 的 Streaming）
- **数据展示页**：图表、表格
- **产品原型 / 内部工具**

> [!tip] FDE 的 React 哲学
> 目标不是把 UI 做到像素级完美，而是 **尽快让客户看到东西在跑**。先用组件库，再谈定制。

---

## 四、配合 Next.js 更省事

单独用 React 需要自己配构建与路由。直接用 [[Next.js]] 可一站式解决：
- 文件路由
- 内置 API Route（可写后端）
- 服务端渲染（首屏更快）

---

## 五、常见坑

> [!warning]
> - **无限渲染循环**：`useEffect` 依赖写错，导致反复请求。
> - **key 用 index**：列表渲染用数组下标做 key，数据重排时出 bug，用稳定 id。
> - **忘了 loading / error 态**：Demo 时接口慢或挂了，界面一片空白，客户体验差。

## 六、组件交付标准

- Props 和状态边界清楚，异步状态不会被重复提交或竞态覆盖。
- 组件包含默认、加载、空、失败、禁用和权限不足状态。
- 表单错误与服务端校验一致，不只在浏览器端拦截。
- 关键交互有键盘路径、可读标签和稳定的测试选择器。
- 视觉回归或 E2E 只保护业务关键路径，避免快照噪声。

---

相关笔记：
- [[Next.js]] —— React 的全栈落地
- [[Tailwind CSS]] —— 快速样式
- [[TypeScript]] —— React 的现代写法
- [[FDE 学习路线]] —— 第二阶段
