---
title: Palantir Ontology 三层架构
aliases: [Ontology 三层结构, 语义层, 动力层, 动态层, Semantic Kinetic Dynamic]
tags: [fde, palantir, ontology, architecture]
created: 2026-09-04
type: guide
domain: topic
layer: advanced
canonical: false
status: evolving
updated: 2026-09-15
sources: []
---

# Palantir Ontology 三层架构

> [!abstract] 一句话
> Palantir Ontology 由**语义层（Semantic）**、**动力层（Kinetic）**、**动态层（Dynamic）** 三层构成，分别回答"世界里有什么"、"我们能做什么"、"AI 如何推理"。

---

## 一、语义层（Semantic）——"世界里有什么"

### 定义

将企业异构数据源映射为统一的实体和关系，形成知识图谱。

### 核心元素

| 元素 | 说明 | 示例 |
|---|---|---|
| **Object Type** | 业务实体类别 | `Supplier`、`PurchaseOrder`、`Part`、`Shipment` |
| **Property** | 实体属性 | 订单金额、交付日期、供应商评级、库存数量 |
| **Link Type** | 实体间关系 | `Supplier —[supplies]→ Part`、`Order —[contains]→ Part` |
| **Object Set** | 动态对象集合 | "未来 14 天内存在延迟风险的订单集合" |

### 映射机制

通过 **Kinect 映射引擎**建立双向语义映射：
- 不是把数据搬到新仓库，而是在源头建立映射
- 源系统数据更新时，Ontology 自动同步
- 用户通过 Ontology 修改数据时，变更回写到源系统
- 保证"数字孪生"与物理系统的一致性

### 数据源类型

| 数据源 | 典型系统 |
|---|---|
| ERP | SAP、Oracle EBS |
| CRM | Salesforce、HubSpot |
| IoT 传感器 | 工业传感器、GPS |
| 电子表格 | Excel、Google Sheets |
| 外部 API | 天气、汇率、物流追踪 |
| 数据湖 | Iceberg、Parquet、Delta |

### 关键认知

> [!note] Ontology 不是数据库 schema
> 数据库 schema 关心数据如何存储，Ontology 关心业务世界如何被理解和操作。
>
> [!note] Ontology 不是普通知识图谱
> 知识图谱强调实体关系的表达，Palantir Ontology 还要包含权限、动作、工作流和应用行为。

---

## 二、动力层（Kinetic）——"我们能做什么"

### 定义

将只读的语义层扩展为可操作系统，定义用户和 AI Agent 可以执行的受控操作。

> [!tip] 这是 Palantir 与传统数据建模最关键的区别
> 传统方案：看完数据再想怎么行动。
> Ontology：数据、行动、规则、权限在同一个模型里。

### 核心元素

#### Action Type（操作类型）

定义用户或 AI Agent 可以对对象执行的操作，带完整的治理机制：

| 特性 | 说明 |
|---|---|
| **验证规则** | 操作前校验数据合法性（如：库存>0 才能创建订单） |
| **业务约束** | 业务逻辑限制（如：>500 元退款需要区域经理审批） |
| **副作用** | 操作触发的后续动作（如：审批通过后自动通知供应商） |
| **审计追踪** | 记录谁在什么时间执行了什么操作 |
| **权限控制** | 操作级权限（如：只有店长能执行 `TransferEmployee`） |

#### Function（函数）

TypeScript/Python 服务端逻辑，直接操作本体对象：
- 读取对象属性、遍历关系
- 执行复杂计算（风险评分、成本优化）
- 作为 LLM Tool 被 AIP 调用

#### 回写机制（Writeback）

当 Ontology 中的操作需要更新源系统时：
- 通过 Webhook 调用外部系统 API
- 仅在外部系统成功响应后才更新 Ontology 内部状态
- 确保"数字 twin"永远不偏离物理系统的真实状态

### 场景示例

| 对象 | 可执行操作 |
|---|---|
| `Order` | `标记风险`、`调整优先级`、`发起审批`、`创建补货任务` |
| `Equipment` | `创建维修工单`、`更新状态`、`关闭告警` |
| `Employee` | `调店`、`排班变更`、`培训记录更新` |

---

## 三、动态层（Dynamic）——"AI 如何推理"

### 定义

AI 模型、模拟分析和 AIP Logic 在这一层运行，将实时数据和逻辑结合，执行 What-If 场景分析和自动化推理。

### 核心能力

#### OAG（Ontology Augmented Generation）

类似 RAG，但不只是检索文档，而是检索和操作结构化业务对象：

- **Query Objects**：LLM 自主从 Ontology 搜索所需数据
- **Calculator**：调用计算器工具获取精确数值
- **Apply Action**：基于推理结果修改实际数据或写回外部系统

> [!warning] 与普通 RAG 的区别
> 普通 RAG：LLM 从文档中检索相关段落，生成回答。
> OAG：LLM 从 Ontology 中检索结构化对象，执行操作，有审计追踪。

#### Scenario Branching（场景分支）

类似 Git 的分支机制：
- AI 提出的变更存在于分支上
- 人类审查后才合并到主线
- 分支里跑的操作也走权限校验
- Scenario 创建后不可变

> 这就是 Palantir 说的"给现实世界做版本控制"。

#### AIP Logic

确定性工具（计算器、优化器、ML 模型）与 LLM 的结合：
- LLM 负责理解意图、规划步骤
- 确定性工具负责精确计算
- 结果通过 Ontology 的权限和审计体系执行

---

## 四、三层如何协同

```
┌─────────────────────────────────────────┐
│           动态层 (Dynamic)               │
│   AI 推理 / OAG / Scenario / AIP Logic  │
├─────────────────────────────────────────┤
│           动力层 (Kinetic)               │
│     Action Type / Function / Writeback  │
├─────────────────────────────────────────┤
│           语义层 (Semantic)              │
│   Object Type / Property / Link Type    │
├─────────────────────────────────────────┤
│           数据源层 (Data Sources)        │
│   ERP / CRM / IoT / Excel / API / Lake  │
└─────────────────────────────────────────┘
```

**数据流**：
1. 数据源 → 语义层：映射为统一对象
2. 语义层 → 动力层：对象可被操作
3. 动力层 → 动态层：AI 可基于对象推理和执行
4. 动态层 → 语义层：AI 操作结果更新对象状态
5. 语义层 → 数据源：变更回写到源系统

---

## 五、后端架构概览

Ontology 后端由多个微服务组成：

| 服务 | 职责 |
|---|---|
| **OMS（Ontology Metadata Service）** | 定义 Ontology 实体的元数据（对象类型、链接类型、操作类型等） |
| **Object Storage V2** | 索引和存储对象数据，支持快速查询 |
| **OSS（Object Set Service）** | 处理动态/静态对象集的查询和过滤 |
| **Object Data Funnel** | 编排数据写入，从数据源读取并索引到对象数据库 |
| **Actions** | 执行用户和 Agent 的操作，应用验证规则和副作用 |
| **Functions** | 在受控环境中运行 TypeScript/Python 业务逻辑 |

> [!note] 不是图数据库
> 业务视角上的"图"不等于部署一套 Neo4j。Ontology 后端是多服务协同的微服务架构。

---

## 六、相关笔记

- [[Palantir Ontology 核心概念]] —— 总览
- [[Palantir Ontology 与传统方案对比]] —— 区别在哪
- [[Palantir AIP 与 AI 集成]] —— AI 如何使用 Ontology
- [[Palantir FDE 与 Ontology]] —— FDE 模式
- [[企业系统集成]] —— 更广泛的集成话题
- [[Agent]] —— AI Agent 基础
- [[Tool Calling]] —— LLM 工具调用
