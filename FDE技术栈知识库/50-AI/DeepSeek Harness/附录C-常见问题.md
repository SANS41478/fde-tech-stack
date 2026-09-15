---
title: 常见问题 — FAQ
aliases:
  - FAQ
  - 问题
tags:
  - deepseek-harness
  - FAQ
  - 附录
created: 2026-08-31
type: reference
domain: ai
layer: implementation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# 附录 C — 常见问题

---

## Q1：我完全没学过编程，能看懂这个系列吗？

**A**：可以。这个系列是为零基础设计的。每篇都从日常类比开始，不假设你有任何编程知识。但如果你完全没接触过编程，建议在读 [[04-TypeScript 速成]] 时多花点时间，因为后面的章节会频繁出现代码。

---

## Q2：为什么要学 TypeScript？Python 不行吗？

**A**：Harness 是用 TypeScript 写的，所以你需要能读懂 TS 代码才能理解源码。但如果你想**自己写 Agent**（而不是修改 Harness），Python 完全可以。[[15-从零写一个最小 Agent]] 就是 Python 版的。

---

## Q3：Harness 和 Claude Code / Cursor 有什么区别？

**A**：它们都是 Agent 工具，但定位不同：

| 工具 | 定位 |
|---|---|
| Claude Code | Anthropic 的官方 Agent 工具 |
| Cursor | AI 辅助的代码编辑器 |
| DeepSeek Harness | 通用的 Agent 框架（可定制） |

Harness 的特点是**一切皆插件**，你可以换掉模型、工具、循环本身。其他工具更偏向"开箱即用"。

---

## Q4：我需要 DeepSeek API Key 才能学习这个系列吗？

**A**：**不需要**。前 14 章都是概念讲解，不需要写代码。只有 [[15-从零写一个最小 Agent]] 需要 API Key 来运行实际代码。你也可以跳过那一章，只看代码讲解。

---

## Q5：Cordis 是什么？为什么要用它？

**A**：Cordis 是 Harness 的底层框架，提供插件系统、依赖注入、事件系统。它的设计思想是"一切皆插件"——模型、工具、日志、循环本身都是可替换的插件。这让 Harness 非常灵活，但也增加了学习曲线。

详细讲解见 [[06-Cordis 插件系统]]。

---

## Q6：54 个包太多了，我需要全部学吗？

**A**：**不需要**。你只需要理解以下核心包：

1. `core/agent-loop` — Agent 循环
2. `core/tools` — 工具系统
3. `core/session` — 日志系统
4. `core/system-prompt` — 上下文组装
5. `llm/llm` — LLM 适配

其他包都是在这个基础上的扩展。需要时再查 [[附录B-源码地图]]。

---

## Q7：Agent Loop 的"Loop"是什么意思？

**A**：Loop = 循环 = 反复执行同一段代码。Agent Loop 就是 Agent 反复执行"接收消息 → 调用 LLM → 执行工具"这个过程，直到 LLM 给出最终回答。

详细讲解见 [[07-Agent Loop 深度拆解]]。

---

## Q8：为什么 Session Log 要记录每一个 token？

**A**：为了**完美回放**。如果只记录完整消息，你就无法重现 LLM 的逐字输出过程。记录每个 token 后，你可以：
1. 精确回放对话（包括打字效果）
2. 分析 LLM 的生成过程
3. 从断点恢复（如果程序崩溃）

详细讲解见 [[09-Session 日志]]。

---

## Q9：子 Agent 和普通 Agent 有什么区别？

**A**：子 Agent 是由主 Agent 创建的"助手"，用于委派子任务。它有独立的 Session Log 和工具集，但受主 Agent 管理。完成后，结果返回主 Agent。

详细讲解见 [[11-子 Agent 与多 Agent]]。

---

## Q10：我想开发自己的 Agent 框架，从哪里开始？

**A**：建议的学习路径：

1. 先完成这个系列（理解 Harness 的设计思想）
2. 用 Python 写一个最小 Agent（[[15-从零写一个最小 Agent]]）
3. 逐步添加功能：日志、工具、插件系统
4. 参考 Harness 的源码，但不一定要用 TypeScript
5. 考虑使用现有的框架（如 LangChain）作为基础

---

## Q11：Harness 是用什么语言写的？

**A**：TypeScript，运行在 Node.js 上。所有源码都在 `packages/` 目录下。

---

## Q12：为什么 Harness 用"事件"而不是直接函数调用？

**A**：事件系统有几个好处：

1. **松耦合**：插件不需要知道谁在监听事件
2. **可扩展**：任何人都可以添加新的事件监听器
3. **可逆**：监听器可以随时移除
4. **可组合**：多个监听器可以协作处理同一个事件

详细讲解见 [[06-Cordis 插件系统]]。

---

## Q13：如何调试 Harness 的 Agent Loop？

**A**：

1. 查看 Session Log：每个事件都有记录
2. 使用 `--dump-config` 查看插件树
3. 添加日志输出到相关插件
4. 使用 Creator 模式实时检查状态

---

## Q14：Harness 支持哪些 LLM？

**A**：理论上支持所有 LLM，只要实现对应的适配器。内置支持：

- DeepSeek（原生）
- OpenAI
- Anthropic
- Bedrock
- Vertex
- Azure
- Ollama

详细讲解见 [[02-核心概念]]。

---

## Q15：这个系列适合什么水平的人？

**A**：

| 水平 | 适合章节 |
|---|---|
| 完全零基础 | 01-03（概念入门）|
| 有基础但不会编程 | 01-06（概念 + 技术基础）|
| 会编程但不会 TS | 04-10（TS 速成 + 核心机制）|
| 会 TS 想深入 | 07-14（源码级讲解）|
| 想动手实践 | 15（从零写 Agent）|

---

## 相关笔记

- [[00-学习路线图]] — 总览
- [[附录A-术语表]] — 术语查询
- [[附录B-源码地图]] — 包功能索引
