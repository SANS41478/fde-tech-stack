---
title: RAG
aliases: [检索增强生成, Retrieval-Augmented Generation, RAG 流程]
tags: [fde, ai, rag, retrieval]
created: 2026-08-24
type: reference
domain: ai
layer: foundation
canonical: true
canonical_group: ai-rag
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://platform.openai.com/docs/overview]
---

# RAG（检索增强生成）

> [!abstract] 定位
> **RAG（Retrieval-Augmented Generation，检索增强生成）** 让 LLM 基于 **私有/最新知识** 回答，而不是只靠训练记忆。对 FDE 来说，它是「把客户文档变成可问答能力」的最常见打法——企业知识库、合同问答、内部手册都靠它。

> [!info] 本文边界
> **负责**：RAG 基础管线、组件、选型和质量检查。<br>
> **不负责**：Agent 主导的迭代检索与结构化知识更新（见 [[Agentic RAG]]）。

---

## 一、完整流程

```text
Documents
   ↓ Parsing（解析 PDF/Word/网页）
Chunking（分块）
   ↓ Embedding（向量化，见 [[Embedding]]）
Vector Database（[[PostgreSQL]] pgvector / Qdrant / Pinecone）
   ↓ Retrieval（相似检索）
LLM（结合检索内容生成，见 [[LLM API]]）
   ↓
Answer
```

---

## 二、关键环节详解

### 1. Parsing
把 PDF / 网页 / Word 转成纯文本。表格、图片常是难点，需专门处理。

### 2. Chunking（分块）
- 太大：检索不精准、超出上下文。
- 太小：语义断裂。
- 常用：按段落 / 固定 token 数（如 512）+ 重叠（overlap）防割裂。

### 3. Embedding + 向量库
见 [[Embedding]]。把每块文本变成向量，存进向量库。

### 4. Retrieval（检索）
- **Similarity Search**：余弦相似度找最相关块。
- **Metadata Filtering**：先按部门/时间/权限过滤，再检索（企业必备）。
- **Hybrid Search**：向量 + 关键词（BM25）结合，弥补纯向量对专有名词的弱。
- **Reranking**：先用粗排取 Top-N，再用交叉编码器精排。

### 5. Generation
把检索到的块拼进 prompt（见 [[Prompt 工程]]），让模型基于「有出处」的内容回答，并可要求引用来源。

---

## 三、FDE 常见技术选型

```text
pgvector      # 已用 [[PostgreSQL]] 就直接上，少引入新组件
Qdrant        # 专业向量库，性能好
Pinecone      # 托管，免运维
Weaviate      # 自带混合检索
```
框架可用 LlamaIndex / LangChain 串流程，但重点理解原理而非背 API。

---

## 四、质量优化清单

> [!tip] 检索质量 = RAG 成败
> - chunk 大小与重叠调优
> - 加 metadata 过滤（权限/领域）
> - 上 hybrid + rerank
> - 评估：用真实问题测「检索到没」「答得对没」

---

## 五、常见坑

> [!warning]
> - **直接把整文档塞 prompt**：贵且噪声大，先检索再喂。
> - **忽略权限**：检索返回了别的部门机密，必须在 metadata 层过滤。
> - **不评估**：只 demo 一个成功例子，真实召回很烂。
> - **embedding 模型与库维度不一致**：换模型要重建索引。

---

## 六、进阶方向（Agentic RAG）

基础 RAG 之上有一整套升级路线，详见 [[Agentic RAG]]：

- **检索管线工程化**：稠密（语义）+ 稀疏（BM25 精确匹配）并行 → RRF 融合 → 跨编码器重排序；用 recall@k / MRR / nDCG 验收。
- **上下文感知检索**：索引前用 LLM 为每个分块生成上下文前缀（"[本段节选自 ACME 2025Q2 财报…]"），解决"该公司指谁"的分块信息丢失——检索失败率可降 49-67%。
- **结构化索引**：RAPTOR（树状层次摘要）/ GraphRAG（实体关系图谱，多跳推理与实体消歧）/ 文件系统范式（L0 摘要 → L1 概览 → L2 全文按需加载）。
- **Agentic RAG**：检索从固定前置步骤变为 Agent 可随时调用的工具——思考 → 检索 → 评估信息是否充分 → 迭代检索 → 综合生成。复杂多跳问题提升显著。
- **知识更新**：增量更新走 Proposer-Reviewer 的 PR 流水线；定期全量整理去重、回到原始证据核查；失效内容在检索层过滤。
- **安全**：被投毒的文档同样是注入通道，见 [[提示注入]]。

## 七、生产级 RAG 验收矩阵

| 维度 | 最小验证 |
| --- | --- |
| 召回 | 每个问题是否召回包含答案的证据块 |
| 排序 | 首屏证据是否足够相关，是否需要重排 |
| 生成 | 回答是否只使用证据，引用是否对应原文 |
| 新鲜度 | 文档更新、删除、权限变化多久生效 |
| 隔离 | 跨租户、跨部门和过期文档是否被过滤 |
| 失败 | 无证据、冲突证据和检索服务故障如何处理 |
| 成本 | 每次查询的 embedding、检索、重排和生成成本 |

评估集应同时包含正常问题、同义改写、拼写错误、跨文档问题、权限边界和“应该拒答”的问题。索引、分块、过滤器或模型改变时，必须重新跑回归。

---

相关笔记：
- [[Embedding]] —— 向量化核心
- [[Agentic RAG]] —— 进阶检索流水线、结构化索引与 Agentic 范式
- [[记忆系统]] —— 双层记忆架构（结构化常驻 + 检索按需）
- [[PostgreSQL]] —— pgvector 落地
- [[LLM API]] / [[Prompt 工程]] —— 生成阶段
- [[FDE 练习项目]] —— 企业知识库项目
