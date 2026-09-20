---
title: SQL
aliases: [sql, SQL 语言, 结构化查询语言, 查询语言]
tags: [fde, database, sql, skill]
created: 2026-08-24
type: reference
domain: data
layer: foundation
canonical: true
canonical_group: data-sql
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: evergreen
sources: [https://www.postgresql.org/docs/current/]
---

# SQL 基础

> [!abstract] 定位
> **SQL（Structured Query Language）** 是与关系型数据库对话的语言。FDE 不必成为 DBA，但必须能 **自己写查询、排查数据问题、设计表结构**——因为客户的数据几乎永远在某种数据库里。

> [!note] 与 [[PostgreSQL]] 的关系
> SQL 是「语言」，PostgreSQL 是「说这种语言的数据库之一」。本篇讲语言本身，落地细节（索引、执行计划）见 PostgreSQL 篇。

---

## 一、FDE 为什么必须会 SQL

- 客户数据在 MySQL / Postgres / SQL Server 里，调 API 拿不全，常要直接查。
- 做数据分析、出报表，SQL 比导出 Excel 快得多。
- 排查「为什么界面显示不对」时，往往要下钻到 SQL 层（见 [[Debugging 与可观测性]]）。
- [[RAG]] 之外，大量 AI 应用是「查数据库 + 让模型总结」，SQL 是底座。

---

## 二、核心语法地图

### 1. 基础查询
```sql
SELECT id, name, created_at
FROM customers
WHERE status = 'active'
ORDER BY created_at DESC
LIMIT 100;
```

### 2. 聚合与分组
```sql
SELECT region, COUNT(*) AS n, AVG(amount) AS avg_amt
FROM orders
GROUP BY region
HAVING COUNT(*) > 10;
```

### 3. 连接（JOIN）
```sql
SELECT o.id, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id;
```

### 4. 窗口函数
```sql
SELECT name, amount,
       RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS rk
FROM orders;
```

### 5. CTE（可读性）
```sql
WITH recent AS (
  SELECT * FROM orders WHERE created_at > now() - interval '7 days'
)
SELECT region, COUNT(*) FROM recent GROUP BY region;
```

---

## 三、FDE 要理解的「非语法」知识

- **执行顺序**：`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`，理解它才能写出对的聚合。
- **索引如何影响查询**：有索引的过滤快，函数包住列（`WHERE YEAR(d)=2024`）会让索引失效。
- **事务与隔离**：多个写操作要么一起成功要么回滚。
- **NULL 语义**：`NULL` 不等于空字符串，也不等于 0，`NULL = NULL` 是未知。

---

## 四、常见坑

> [!warning]
> - **`SELECT *` 进生产**：字段一变就炸，且浪费 IO，显式列名更稳。
> - **忘记 `LIMIT`**：手滑查全表，锁资源、拖慢库。
> - **在应用层做 JOIN**：把两张大表全拉到内存再关联，远慢于数据库 JOIN。
> - **混淆 `WHERE` 与 `HAVING`**：分组前过滤用 WHERE，分组后过滤用 HAVING。

---

相关笔记：
- [[PostgreSQL]] —— 主要落地的数据库
- [[Redis]] —— 非关系型补充
- [[ETL 与数据管道]] —— SQL 在搬运数据中的角色
- [[Debugging 与可观测性]] —— 数据层排查
