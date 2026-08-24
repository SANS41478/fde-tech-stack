---
title: PostgreSQL
aliases: [Postgres, pg, PostgreSQL, 关系型数据库]
tags: [fde, database, sql, relational]
created: 2026-08-24
---

# PostgreSQL

> [!abstract] 定位
> **PostgreSQL** 是 FDE 的主力关系型数据库。它开源、稳定、功能强，既能做业务存储，也能通过扩展（如 pgvector）直接支撑 [[RAG]] 的向量检索，是「一个数据库覆盖多种需求」的性价比之选。

---

## 一、为什么是 PostgreSQL 而非 MySQL/MongoDB

- **功能全面**：JSON 字段、窗口函数、CTE、全文检索都有。
- **扩展生态**：`pgvector` 做向量检索，`PostGIS` 做地理，省去再引入专用库。
- **与 AI 场景契合**：业务表 + 向量列共存，简化架构（见 [[RAG]]、[[Embedding]]）。
- **可靠**：事务、一致性经过长期验证。

> [!tip] FDE 的组合
> 业务数据用 Postgres 表；向量检索用 `pgvector`；缓存 / 队列用 [[Redis]]。三者 + [[FastAPI]] + [[Docker Compose]] 一条命令起来。

---

## 二、必会 SQL 能力

参见 [[SQL]] 专篇，这里列 Postgres 重点：

```sql
SELECT ... JOIN ...          -- 关联查询
GROUP BY / 聚合              -- 统计
WINDOW FUNCTION (OVER)       -- 排名、累计
CTE (WITH ...)               -- 可读的子查询
INDEX                        -- 加速
TRANSACTION                  -- 一致性
EXPLAIN / EXPLAIN ANALYZE    -- 看执行计划
```

---

## 三、不只是「会写 SQL」

FDE 还要理解：

- **表结构设计**：范式 vs 反范式，按查询模式建表。
- **索引**：哪些列建索引、联合索引顺序、避免索引失效。
- **查询性能**：慢查询用 `EXPLAIN` 定位，别靠猜。
- **数据一致性**：事务边界、外键、约束。
- **权限**：给应用账号最小权限，别用 superuser。
- **备份 / 恢复**：交付前确认有备份策略。

---

## 四、和 AI 的结合（pgvector）

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE docs (id serial, content text, embedding vector(1536));
-- 相似度检索
SELECT content FROM docs
ORDER BY embedding <-> :query_vec LIMIT 5;
```
> 这正是 [[RAG]] 的存储层；配合 [[Embedding]] 模型生成向量。

---

## 五、部署与运维

- 本地 / 测试：[[Docker]] 起一个 Postgres 容器。
- 生产：云托管（见 [[云平台]] 的 RDS / Cloud SQL），或自建 + 备份。
- 迁移：用 Alembic（Python）或 migrate 工具管理 schema 变更，纳入 [[Git]]。

---

## 六、常见坑

> [!warning]
> - **N+1 查询**：循环里查库，性能雪崩，用 JOIN 或批量。
> - **忘记建索引**：上线后数据量一大就慢。
> - **事务过长**：锁表、连接占满。
> - **把向量维度和模型不匹配**：embedding 维度（如 1536）必须和模型一致。

---

相关笔记：
- [[SQL]] —— 查询语言基础
- [[Redis]] —— 缓存 / 队列
- [[RAG]] / [[Embedding]] —— pgvector 应用
- [[Docker Compose]] —— 一键起服务
