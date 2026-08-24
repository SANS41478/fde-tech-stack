---
title: Tailwind CSS
aliases: [Tailwind, tailwindcss, 原子化 CSS]
tags: [fde, frontend, css]
created: 2026-08-24
---

# Tailwind CSS

> [!abstract] 定位
> **Tailwind CSS** 是原子化（utility-first）CSS 框架。FDE 用它可以在不写一堆自定义 CSS 的前提下，快速拼出整洁、一致的界面——是「快速出 Demo」的加速器。

---

## 一、它解决了什么痛点

传统写界面：先想类名 → 写 CSS 文件 → 调样式，循环往复。
Tailwind：直接在 HTML/JSX 里用预定义类，样式即结构。

```tsx
<button className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
  提交
</button>
```

> [!tip] FDE 收益
> 不必在「业务逻辑」和「CSS 调试」之间来回切换。界面一致性由设计系统（间距、颜色 token）保证。

---

## 二、核心概念

- **Utility 类**：`flex`、`p-4`、`text-sm`、`bg-gray-100` 等，每个类只做一件事。
- **响应式**：`md:grid-cols-2` 表示中等屏幕两列。
- **状态变体**：`hover:`、`focus:`、`disabled:` 直接修饰。
- **暗色模式**：`dark:` 前缀，配合主题切换。

---

## 三、FDE 怎么用

和 [[React]] / [[Next.js]] 配合最常见：

```tsx
<div className="mx-auto max-w-2xl p-6">
  <h1 className="text-2xl font-bold">客户工单分析</h1>
  <div className="mt-4 grid gap-4 md:grid-cols-2">
    {/* 卡片列表 */}
  </div>
</div>
```

进一步可用 **shadcn/ui**：基于 Tailwind 的高质量组件库，复制即用，快速出「不像 Demo」的专业界面。

---

## 四、为什么不「手写 CSS」

> [!note]
> FDE 的目标是尽快让客户看到能跑的东西，而不是打磨样式工程。Tailwind 让你把注意力留在功能与价值验证上。等项目真的要产品化，再考虑设计系统也不迟。

---

## 五、常见坑

> [!warning]
> - **类名过长**：JSX 里 class 串很长，可用组件封装或 `cn()` 工具函数。
> - **忘了配置 content 路径**：Tailwind 扫不到文件就不生成样式，检查 `tailwind.config` 的 `content`。
> - **和 UI 库冲突**：某些组件库自带样式，混用时注意优先级。

---

相关笔记：
- [[React]] —— Tailwind 的主战场
- [[Next.js]] —— 一并搭建
- [[FDE 学习路线]] —— 第二阶段加速项
