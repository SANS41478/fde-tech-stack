---
title: Redis
aliases: [redis, Redis 缓存, 内存数据库]
tags: [fde, database, cache, nosql]
created: 2026-08-24
---

# Redis

> [!abstract] 定位
> **Redis** 是内存键值存储。FDE 不一定用它做主存储，但它是 **缓存、会话、队列、限流、临时状态** 的瑞士军刀，几乎每个稍大的 FDE 项目都会碰到。

---

## 一、Redis 解决什么

关系型数据库（[[PostgreSQL]]）强在一致性，弱在「高频小读写」和「临时状态」。Redis 把数据放内存，微秒级响应，补足这块。

常见用途：
```text
Cache        # 缓存热点数据，减压数据库
Session      # 用户登录态
Queue        # 简单任务队列（List / Stream）
Rate Limit   # 接口限流计数器
Temporary State  # Agent 中间状态、验证码
```

---

## 二、FDE 常用数据结构

- **String**：计数器、缓存 JSON、限流 `INCR`。
- **Hash**：存对象（如用户信息）。
- **List**：简单队列（`LPUSH` / `RPOP`）。
- **Set / Sorted Set**：去重、排行榜、延迟队列（ZSET + 时间戳）。
- **Stream**：更可靠的消息队列（配合 [[Agent]] 任务分发）。
- **TTL**：给键设过期时间，天然适合缓存与临时态。

---

## 三、典型场景示例

### 限流（保护下游 [[LLM API]]）
```bash
# 每分钟最多 60 次
INCR rate:user:123
EXPIRE rate:user:123 60
```
超过阈值就拒绝或排队。

### 缓存
```python
val = redis.get("ticket:1")
if not val:
    val = db.query(...)
    redis.setex("ticket:1", 300, val)  # 缓存 5 分钟
```

### 任务队列（配合 Worker）
```text
Producer → LPUSH queue → RPOP → Worker
```
> 大规模用 Stream / 专业队列（Celery + Redis）更稳，思路见 [[ETL 与数据管道]]。

---

## 四、与 AI / Agent 的关系

- **Agent 短期记忆**：把对话历史、工具调用结果放 Redis，带 TTL，避免无限增长（见 [[Agent]]、[[MCP]]）。
- **并发控制**：多 worker 抢任务时的锁（`SET NX`）。

---

## 五、常见坑

> [!warning]
> - **把 Redis 当主库**：内存贵且默认不持久化，重要数据必须落 [[PostgreSQL]]。
> - **忘了设 TTL**：缓存 / 临时态无限增长，内存撑爆。
> - **缓存击穿 / 雪崩**：热点 key 同时失效，瞬间压垮后端，用随机 TTL、互斥重建。
> - **持久化误解**：开了 AOF/RDB 也不等于绝对安全，按重要级配置。

---

相关笔记：
- [[PostgreSQL]] —— 主存储
- [[ETL 与数据管道]] —— 队列 / Worker 模式
- [[Agent]] —— 短期记忆载体
- [[Docker Compose]] —— 一键起 Redis
