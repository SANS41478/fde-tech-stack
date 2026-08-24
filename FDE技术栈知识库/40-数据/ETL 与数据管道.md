---
title: ETL 与数据管道
aliases: [ETL, ELT, Data Pipeline, 数据管道, 数据流水线]
tags: [fde, data, pipeline, integration]
created: 2026-08-24
---

# ETL 与数据管道

> [!abstract] 定位
> **ETL（Extract-Transform-Load）** 与 **数据管道** 是让数据在系统间流动的能力。FDE 做客户集成时，常常要把 A 系统的数据搬进 B 系统、清洗后再喂给 [[LLM API]] 或仪表盘——这就是数据管道的工作。

---

## 一、ETL vs ELT

- **ETL**：先抽取 → 转换（清洗/聚合）→ 再加载到目标。适合目标库弱、需在途中加工。
- **ELT**：先抽取加载到目标（如数仓）→ 在目标里用 SQL 转换。适合 [[PostgreSQL]] / 云数仓算力强。

> [!note] FDE 的现实
> 多数 FDE 场景是「轻 ETL」：从客户 API / 文件抽数据，简单清洗，写库或喂模型。别一上来就搭大数据平台。

---

## 二、FDE 常见的管道形态

```text
Data Source (CRM / 文件 / DB)
     ↓  Extract
Queue / Buffer ([[Redis]] / Kafka)
     ↓  Transform
Worker ([[Python]] / Node)
     ↓  Load
Database ([[PostgreSQL]]) / LLM / Dashboard
```

当要「每天处理 100 万条客户数据再用 AI 分析」时，思路是：
```text
Data Source → Queue → Worker → LLM → Database → Result → Dashboard
```

---

## 三、核心技术点

- **抽取**：调 [[REST API]]（分页、鉴权见 [[OAuth]]）、读文件、连库（[[SQL]]）。
- **转换**：清洗、去重、字段映射、[[Structured Output]] 解析。
- **加载**：批量写库、upsert 防重复。
- **调度**：[[Cron]] 定时跑，或事件触发（[[Webhook]]）。
- **容错**：失败重试、幂等、断点续跑。
- **可观测**：每步计数与日志（见 [[Debugging 与可观测性]]）。

---

## 四、进阶技术（按需）

```text
ClickHouse      # 海量分析型列存
BigQuery        # GCP 数仓
Snowflake       # 云数仓
MongoDB         # 文档型，半结构化数据
```
以及概念：Data Warehouse（数仓）、Streaming（流式）、Batch（批处理）。

> [!tip] FDE 策略
> 不需要一开始全精通，但要有 **快速适应能力**——客户用啥你能在几天内接上。

---

## 五、常见坑

> [!warning]
> - **非幂等加载**：重跑产生重复数据，用 upsert / 唯一键。
> - **全量重跑**：百万数据每次全量，慢且易错，做增量（时间戳 / CDC）。
> - **无监控**：管道静默失败几天才发现，必须加计数与告警。
> - **内存爆**：一次性 `SELECT *` 全拉，用流式 / 分批。

---

相关笔记：
- [[Redis]] —— 队列 / 缓冲
- [[Cron]] —— 定时调度
- [[Webhook]] —— 事件触发
- [[企业系统集成]] —— 数据从哪来
- [[System Design]] —— 管道的容量与可靠性设计
