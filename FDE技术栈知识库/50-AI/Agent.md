---
title: Agent
aliases: [智能体, AI Agent, LLM Agent, Agent 系统]
tags: [fde, ai, agent, automation]
created: 2026-08-24
---

# Agent（智能体）

> [!abstract] 定位
> **Agent（智能体）** 是能 **自主规划、调用工具、观察结果、迭代执行** 以完成目标的系统。相比「一问一答」，Agent 能跑多步流程——这对 FDE 做复杂客户任务（如「查数据→分析→生成报告→发 Slack」）极有价值。

---

## 一、典型结构

```text
User
 ↓
LLM（大脑，做决策）
 ↓
Agent
 ├── Search       # 搜索
 ├── Database     # 查 [[PostgreSQL]]
 ├── API          # 调 [[REST API]]
 ├── File         # 读写文件
 ├── Browser      # [[Playwright]]
 └── External Tool# 任意 [[Tool Calling]]
```

---

## 二、Agent 的运转：Agent Loop

```text
感知目标
  ↓
规划（Plan）：拆成子任务
  ↓
选择工具（Tool Selection）：调哪个？
  ↓
执行工具（Action）：真正干活
  ↓
观察结果（Observation）：拿到反馈
  ↓
再规划 → 循环，直到完成
```

这就是 **ReAct（Reason + Act）** 模式的核心。每轮：模型reasoning → 选动作 → 环境返回观察 → 下一轮。

> [!note] 工具调用的循环化
> 把 [[Tool Calling]] 放进循环，并在每轮回传观察，就得到了 Agent。理解这点比记框架重要。

---

## 三、必须理解的组成

- **Tool Calling**：动作的执行接口（见 [[Tool Calling]]）。
- **Memory（记忆）**：短期（当前对话/任务上下文）、长期（跨会话，常存 [[Redis]] 或向量库）。
- **Planning（规划）**：把大目标拆小；可让模型先列步骤。
- **Tool Selection**：从可用工具中挑对的；工具描述要清楚。
- **反思 / 自我纠正**：工具报错时，让模型读错误再试，而非直接放弃。

---

## 四、FDE 相关技术（理解优先）

```text
LangChain       # 流程编排，生态最大
LlamaIndex      # 数据/RAG 向 Agent
LiteLLM         # 多模型统一网关
MCP             # 工具标准化协议（见 [[MCP]]）
```
> [!tip] 重点不是背 API
> 更重要是理解：**模型如何调用工具、如何获取数据、如何执行操作、如何形成完整工作流。**

---

## 五、设计可靠 Agent 的要点

- **明确终止条件**：别让 Agent 无限循环，设最大步数。
- **工具幂等 + 超时**：见 [[Tool Calling]]。
- **人类兜底**：高风险动作（删、发、钱）加确认。
- **日志可观测**：每一步留痕，出问题能复盘（见 [[Debugging 与可观测性]]）。

---

## 六、常见坑

> [!warning]
> - **过度自主**：让 Agent 自由发挥，结果不可控；给清晰目标与约束。
> - **循环不收敛**：没设 max step，烧钱又卡死。
> - **工具描述含糊**：模型选错工具，任务跑偏。
> - **无记忆管理**：上下文无限增长，超窗口或变贵，用 [[Redis]] 截断。

---

相关笔记：
- [[Tool Calling]] —— Agent 的动作机制
- [[MCP]] —— 工具标准化
- [[RAG]] / [[Playwright]] —— 典型工具
- [[FDE 练习项目]] —— 浏览器自动化 Agent 项目
