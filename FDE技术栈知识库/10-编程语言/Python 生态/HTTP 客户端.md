---
title: HTTP 客户端（requests / httpx）
aliases: [requests, httpx, HTTP 客户端, Python HTTP]
tags: [fde, python, http, integration]
created: 2026-08-24
type: reference
domain: language
layer: foundation
canonical: false
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: evergreen
sources: [https://docs.python.org/3/]
---

# HTTP 客户端（requests / httpx）

> [!abstract] 定位
> 在 Python 里 **发送 HTTP 请求** 的两个主力库：`requests` 是同步经典款，`httpx` 兼容其 API 且额外支持 **异步** 与 **HTTP/2**。FDE 做外部系统对接时，几乎所有「调别人接口」的动作都靠它们。

---

## 一、为什么 FDE 必须会

FDE 的核心动作之一就是「把不同系统连起来」。无论调 [[REST API]]、接 [[SaaS 集成]]、做 [[企业系统集成]]、还是处理 [[Webhook]] 回调，第一步常常是发一个 HTTP 请求：

- 拉客户 CRM / ERP 数据
- 调 [[LLM API]]（本质上也是 HTTP）
- 把结果推到 Slack / 飞书
- 探活、测试、排查接口问题（见 [[Debugging 与可观测性]]）

> [!tip] 选型
> 新项目直接用 **httpx**：API 与 requests 几乎一致，但能 `async` 并发，配合 [[asyncio]] 在高并发调模型/接口时收益巨大。老代码维护继续用 requests 即可。

---

## 二、requests 核心用法

```python
import requests

r = requests.get(
    "https://api.example.com/orders",
    params={"status": "open"},          # 查询参数
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=10,                          # 务必设超时，单位秒
)
r.raise_for_status()                    # 非 2xx 抛异常
data = r.json()                         # 解析 JSON
```

- **Session 复用连接**：`with requests.Session() as s:` 在高并发/多次请求时显著提速。
- **POST + JSON**：`requests.post(url, json=payload)`（自动设 `Content-Type: application/json`）。
- **auth**：支持 `auth=(user, pwd)` 或自定义。

---

## 三、httpx 核心用法（含异步）

```python
import httpx, asyncio

# 同步（与 requests 用法几乎一致）
r = httpx.get(url, timeout=10)

# 异步：并发调 100 个接口
async def main(urls):
    async with httpx.AsyncClient(timeout=10) as c:
        tasks = [c.get(u) for u in urls]
        results = await asyncio.gather(*tasks)
```

> 异步客户端需在事件循环里用（`async def` + `await`），详见 [[asyncio]]。

---

## 四、FDE 实战要点

- **超时必设**：不设 `timeout`，对端卡住时你的程序也永远挂起。
- **状态码必查**：`raise_for_status()` 或手动判断，别假设一定成功。
- **限流与重试**：外部 API 常限流（429），用指数退避重试，避免雪崩（见 [[System Design]]）。
- **密钥走环境变量**：`TOKEN = os.getenv("API_TOKEN")`，绝不硬编码（见 [[企业系统集成]] 安全）。
- **分页要跟**：列表接口几乎都分页，循环拉全（用 [[ETL 与数据管道]] 思路）。

---

## 五、常见坑

> [!warning]
> - **不设 timeout**：对端无响应 → 线程永久阻塞，生产事故。
> - **`json=` 与 `data=` 混淆**：发 JSON 用 `json=`，发表单/原始体用 `data=`，错配会 400。
> - **忽略 HTTPS 校验关闭**：`verify=False` 仅临时调试，生产关校验有中间人风险。
> - **同步库放进异步服务**：在 [[FastAPI]] 协程里用 `requests` 会卡死事件循环，改用 httpx async。
> - **重试不幂等**：POST 重试可能重复创建，关键写操作用 idempotency key。

---

相关笔记：
- [[Python]] —— 所属语言
- [[asyncio]] —— httpx 异步基础
- [[REST API]] —— 请求语义（动词/状态码）
- [[FastAPI]] —— 服务端视角
- [[企业系统集成]] / [[SaaS 集成]] —— 对接对象
