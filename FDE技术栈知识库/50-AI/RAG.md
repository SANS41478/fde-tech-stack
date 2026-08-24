---
title: RAG
aliases: [检索增强生成, Retrieval-Augmented Generation, RAG 流程]
tags: [fde, ai, rag, retrieval]
created: 2026-08-24
---

# RAG（检索增强生成）

> [!abstract] 定位
> **RAG（Retrieval-Augmented Generation，检索增强生成）** 让 LLM 基于 **私有/最新知识** 回答，而不是只靠训练记忆。对 FDE 来说，它是「把客户文档变成可问答能力」的最常见打法——企业知识库、合同问答、内部手册都靠它。

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

相关笔记：
- [[Embedding]] —— 向量化核心
- [[PostgreSQL]] —— pgvector 落地
- [[LLM API]] / [[Prompt 工程]] —— 生成阶段
- [[FDE 练习项目]] —— 企业知识库项目
