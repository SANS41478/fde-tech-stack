---
title: asyncio
aliases: [asyncio, 异步, 异步并发, async/await]
tags: [fde, python, async, concurrency]
created: 2026-08-24
type: reference
domain: language
layer: foundation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# asyncio（异步并发）

> [!abstract] 定位
> **asyncio** 是 Python 的 **异步并发** 标准库：在单个线程里通过 `async/await` 调度大量 **IO 密集型** 任务，让它们在等待网络/磁盘时不空转。对 FDE 来说，它是「并发调 100 个模型/接口而不慢十倍」的关键。

---

## 一、为什么 FDE 要会

FDE 的工作充满 IO 等待：调 [[LLM API]]、发 HTTP（[[HTTP 客户端]]）、查 [[PostgreSQL]]、访问客户系统。同步写法在等待时白白占用线程；异步写法能 **同时挂起成百上千个等待中的任务**。

- [[FastAPI]] 原生异步，写 async 端点吞吐更高。
- [[Agent]] 并发调用多个工具时靠它提速。
- 批量处理客户数据（每天 100 万条，见 [[System Design]]）几乎必须异步/并发。

---

## 二、核心概念

```python
import asyncio, httpx

async def fetch(c, url):          # async 定义协程
    r = await c.get(url)          # await：挂起，让出控制权
    return r.json()

async def main(urls):
    async with httpx.AsyncClient() as c:
        results = await asyncio.gather(     # 并发跑多个协程
            *(fetch(c, u) for u in urls)
        )
    return results

asyncio.run(main(urls))           # 启动事件循环
```

- **`async def` / `await`**：标记协程与挂起点。
- **事件循环（Event Loop）**：调度所有协程的引擎。
- **`asyncio.gather`**：并发执行多个协程并收集结果。
- **`asyncio.create_task`**：把协程放进循环后台跑。
- **`asyncio.to_thread`**：把阻塞函数丢到线程池，避免卡死循环。

---

## 三、FDE 实战要点

- **只在 IO 密集时用**：CPU 密集（大量计算）异步帮不上忙，考虑多进程。
- **用异步库全家桶**：HTTP 用 httpx async，DB 用异步驱动（[[SQLAlchemy]] AsyncSession），别在协程里塞同步阻塞调用。
- **限流并发数**：`asyncio.gather` 上千任务可能压垮下游，用信号量 `asyncio.Semaphore` 限流（见 [[System Design]]）。

---

## 四、常见坑

> [!warning]
> - **在协程里调阻塞代码**：`requests.get` / `time.sleep` 会卡死整个事件循环，改用 `await httpx` / `await asyncio.sleep`。
> - **忘记 `await`**：协程不执行，静默无结果。
> - **`gather` 一个异常全崩**：用 `return_exceptions=True` 或逐个 try，避免一颗老鼠屎坏一锅。
> - **async 与 sync 库混用混乱**：厘清哪些函数要 `await`，哪些不需要。
> - **调试困难**：异步栈追踪不易读，靠日志 + [[Debugging 与可观测性]]。

---

相关笔记：
- [[Python]] —— 所属语言
- [[HTTP 客户端]] —— httpx 异步搭档
- [[FastAPI]] —— 异步服务端
- [[SQLAlchemy]] —— 异步会话
- [[System Design]] —— 并发与限流设计
