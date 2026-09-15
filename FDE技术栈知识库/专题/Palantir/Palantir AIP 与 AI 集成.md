---
title: Palantir AIP 与 AI 集成
aliases: [AIP, AI Platform, OAG, Ontology Augmented Generation, AI FDE, AIP Logic]
tags: [fde, palantir, ai, ontology, agent]
created: 2026-09-04
type: guide
domain: topic
layer: advanced
canonical: false
status: evolving
updated: 2026-09-15
sources: []
---

# Palantir AIP 与 AI 集成

> [!abstract] 一句话
> **AIP（AI Platform）** 让 LLM 不只是"聊天"，而是能在 Ontology 的结构化业务对象上**查询数据、调用函数、执行操作**，同时受权限和审计约束。这是 Palantir 所说的 **OAG（Ontology Augmented Generation）**。

---

## 一、为什么 LLM 需要 Ontology

### 裸接 LLM 的问题

| 问题 | 说明 |
|---|---|
| **幻觉** | LLM 不知道数据的真实含义，会编造 |
| **无操作能力** | LLM 只能生成文本，不能执行业务操作 |
| **无权限控制** | LLM 可能看到不该看的数据，执行不该执行的操作 |
| **无审计追踪** | LLM 的输出无法追溯到具体决策 |

### LLM + Ontology 的解决方案

| 问题 | Ontology 如何解决 |
|---|---|
| 幻觉 | LLM 查询 Ontology 的结构化对象，不是靠训练数据猜测 |
| 无操作能力 | LLM 可以调用 Action Type 执行业务操作 |
| 无权限控制 | LLM 看到的数据和能执行的操作受 Ontology 权限约束 |
| 无审计追踪 | 每次 AI 操作都有完整审计日志 |

---

## 二、OAG（Ontology Augmented Generation）

### 概念

类似 RAG（检索增强生成），但不只是检索文档，而是检索和操作**结构化业务对象**。

### 工作流程

```
用户输入自然语言请求
    ↓
LLM 理解意图，规划步骤
    ↓
LLM 通过三个核心工具执行：

1. Query Objects —— 从 Ontology 搜索所需数据
2. Calculator —— 调用计算器工具获取精确数值
3. Apply Action —— 基于推理结果修改实际数据或写回外部系统

    ↓
结果通过 Ontology 的权限和审计体系执行
    ↓
人审查后合并（Scenario Branching）
```

### 与普通 RAG 的区别

| 维度 | 普通 RAG | OAG |
|---|---|---|
| 检索对象 | 文档、段落 | 结构化业务对象 |
| 输出 | 文本回答 | 文本 + 操作（如：重新路由订单） |
| 权限 | 无 | 受 Ontology 权限约束 |
| 审计 | 无 | 完整操作审计日志 |
| 确定性 | 低（LLM 可能幻觉） | 高（操作受验证规则约束） |

---

## 三、AIP Logic：确定性与概率性的结合

### 核心思想

LLM 擅长理解意图和规划，但不擅长精确计算。AIP Logic 让两者各司其职：

| 组件 | 职责 |
|---|---|
| **LLM** | 理解自然语言意图、规划执行步骤、生成回答 |
| **确定性工具** | 计算器、优化器、ML 模型——负责精确计算 |
| **Ontology** | 提供结构化数据、操作定义、权限控制 |

### 三个核心工具

| 工具 | 说明 | 示例 |
|---|---|---|
| **Query Objects** | LLM 自主从 Ontology 搜索数据 | "查询所有延迟的订单" |
| **Calculator** | 调用计算器获取精确数值 | "计算这批货物的总成本" |
| **Apply Action** | 基于推理结果执行操作 | "将这批订单标记为高风险" |

### 场景示例：供应链短缺决策

```
用户：这批原材料短缺会影响哪些订单？

LLM 规划：
1. 查询 Ontology 获取原材料库存和关联订单
2. 调用计算器计算影响范围
3. 生成影响报告 + 建议操作

Ontology 执行：
- Query Objects → 获取受影响的订单列表
- Calculator → 计算延迟天数和财务影响
- Apply Action → 建议的操作（加急/替代/调拨）

用户审查：
- 看到影响报告
- 选择执行 AI 建议的操作
- 操作写回 ERP，记录审计日志
```

---

## 四、Scenario Branching：给现实世界做版本控制

### 机制

类似 Git 的分支机制，让 AI 的操作可以被审查：

| 步骤 | 说明 |
|---|---|
| 1. AI 提出变更 | 如："重新路由 50 个订单" |
| 2. 变更存在于分支 | 不直接修改主线数据 |
| 3. 人类审查 | 查看 AI 的建议和理由 |
| 4. 批准后合并 | 分支合并到主线，操作执行 |

### 关键特性

- 分支里跑的操作也走 Role/Classification/Purpose 权限校验
- Scenario 创建后不可变（immutable）
- 不会自动合并回主线——需要人主动操作
- 审计日志记录 AI 的每一步推理

> [!note] 与 Git 的类比
> Palantir 本质上是给企业运营做了 `git`——每个 AI 提议的变更都走一个 "pull request"，人批准后才生效。

---

## 五、AI Agent 在 Ontology 上的工作方式

### Agent 的能力边界

| 能做 | 不能做 |
|---|---|
| 查询 Ontology 对象 | 绕过权限直接访问底层数据库 |
| 调用 Function 执行计算 | 在没有 Action Type 的情况下修改数据 |
| 建议操作（通过 Scenario） | 绕过审批直接执行操作 |
| 读取审计日志 | 删除或修改审计记录 |

### 安全模型

```
用户请求
    ↓
权限检查：用户能看到哪些对象？能执行哪些操作？
    ↓
LLM 只看到用户有权限的数据
    ↓
LLM 建议的操作受 Action Type 的验证规则约束
    ↓
操作记录审计日志
```

> [!warning] AI 不是"直接改系统"
> AIP 的常见落地方式不是"让 AI 直接改系统"，而是：
> 1. AI 分析数据，生成建议
> 2. 人审查建议
> 3. 人批准后，操作通过 Ontology 的 Action 执行
> 4. 操作写回源系统，记录审计

---

## 六、AI FDE：用 AI 模拟 FDE 工作

### 定义

AI FDE 是一个交互式 Agent，通过自然语言命令代为操作 Foundry。

### 能做什么

- 数据转换和管道构建
- 代码仓库管理
- Ontology 构建和维护
- Workshop 应用开发

### 意义

| 之前 | 之后 |
|---|---|
| FDE 驻场几个月 | AI FDE 用自然语言描述，自动执行 |
| 每家客户需要 FDE 时间 | AI FDE 可并行服务多个客户 |
| FDE 数量是瓶颈 | 降低对人力的依赖 |

---

## 七、AIP 的 12 层能力架构

| 层 | 能力 |
|---|---|
| 1 | 安全 LLM 集成（GPT、Gemini、Claude、Llama 等） |
| 2 | 模型管理与评估 |
| 3 | 向量化与计算服务 |
| 4 | **Ontology 系统**（核心） |
| 5 | 向量/计算/工具服务 |
| 6 | 安全与治理 |
| 7 | Agent 生命周期管理 |
| 8 | 开发环境 |
| 9 | 人机协作应用 |
| 10 | 企业自动化 |
| 11 | 可观测性与评估 |
| 12 | 部署与运维（Apollo） |

---

## 八、AI + Ontology 的结合深度评估

> [!note] 客观评价
> **AI 结合得不够深的部分**：
> - Ontology 本身不是 AI 产品，AI 是后来叠上去的
> - 构建 Ontology 仍然高度依赖人工（FDE 驻场）
> - 核心价值不在 AI——Ontology 解决的是数据整合问题
>
> **AI 结合得比较深的部分**：
> - OAG：LLM 直接查询结构化对象、调用 Action
> - Scenario Branching：AI 操作有"pull request"
> - AIP Logic：确定性工具与 LLM 结合
> - AI FDE：AI 辅助构建 Ontology 本身
>
> **本质**：Ontology 不是因为 AI 才有价值的，但它因为 AI 才变得**不可替代**。因为在 AI 时代，你不能让 LLM 直接操作数据库，你需要一个中间层来约束它，Ontology 就是这个中间层。

---

## 九、相关笔记

- [[Palantir Ontology 核心概念]] —— Ontology 总览
- [[Palantir Ontology 三层架构]] —— 动态层详解
- [[Palantir FDE 与 Ontology]] —— FDE 模式
- [[Palantir Ontology 落地案例]] —— 真实场景
- [[LLM API]] —— LLM 调用基础
- [[Tool Calling]] —— LLM 工具调用
- [[Agent]] —— AI Agent 基础
- [[RAG]] —— 检索增强生成
- [[Structured Output]] —— 结构化输出
