---
title: Python
aliases: [python, Py, 派森]
tags: [fde, language, backend, ai]
created: 2026-08-24
type: reference
domain: language
layer: foundation
canonical: true
canonical_group: language-python
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: evergreen
sources: [https://docs.python.org/3/]
---

# Python

> [!abstract] 定位
> 对 AI FDE 来说，**Python 是第一优先级语言**。它不是「最 Fast」或「最底层」，但它是把 AI 生态、数据处理、自动化、API 服务串起来的 **最短路径**。

---

## 一、为什么 Python 是 FDE 第一语言

- **AI 生态几乎全在 Python**：[[LLM API]] 的 SDK、LangChain、LlamaIndex、Embedding 库、向量库客户端，首选都是 Python。
- **写起来快**：客户面前，能在 30 分钟内写出能跑的脚本，比「优雅但慢」有价值。
- **胶水能力强**：既能调 HTTP（[[REST API]]），又能跑pandas，又能 subprocess 调命令行工具。
- **部署简单**：配合 [[FastAPI]] 与 [[Docker]]，后端服务上线极快。

> [!tip] FDE 对 Python 的要求
> 你 **不一定** 要成为 Python 底层专家（如 CPython 源码、GIL 深究）。但要做到一句话：
> **看到一个客户需求，能快速写出一个可以运行的 Python 解决方案。**

---

## 二、FDE 主要用 Python 做什么

- AI 应用（调模型、做 [[Agent]]）
- 数据处理（清洗、转换、聚合）
- 自动化（脚本、定时任务 [[Cron]]）
- API 服务（[[FastAPI]]）
- Web Scraping / 浏览器自动化（配合 [[Playwright]]）
- 快速 Prototype
- 企业系统集成（调客户 [[REST API]]）

---

## 三、建议掌握的技术栈

下面每个子工具都已有独立深度笔记，点开即看：

- [[FastAPI]] —— Web API 框架（Python 后端首选）
- [[HTTP 客户端]] —— requests / httpx，发 HTTP 请求对接外部系统
- [[pandas]] —— DataFrame 数据处理，清洗 / 聚合客户数据
- [[asyncio]] —— 异步并发，高并发调模型 / 接口
- [[subprocess]] —— 调系统命令，粘合客户奇怪的 CLI 工具
- [[Pydantic]] —— 数据校验 / 配置，接口与 LLM 输出落地
- [[SQLAlchemy]] —— ORM / 数据库，操作 [[PostgreSQL]] 数据层
- [[pytest]] —— 测试，快速迭代的保险与 [[CI-CD]] 闸门

### 重点说明
- **HTTP 客户端优先 httpx**：支持异步，配合 [[asyncio]] 在 FDE 高并发调模型时很关键（详见 [[HTTP 客户端]]）。
- **Pydantic**：和 [[FastAPI]] 天然配合，也常用于 [[Structured Output]] 的结果校验。
- **asyncio**：当要并发调 100 个 [[LLM API]] 请求时，同步写法会慢十倍。

---

## 四、FDE 常见代码片段模式

### 1. 快速调一个模型并结构化输出
```python
from pydantic import BaseModel
from openai import OpenAI

class Ticket(BaseModel):
    category: str
    priority: int

client = OpenAI()
resp = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": text}],
    response_format=Ticket,
)
print(resp.choices[0].message.parsed)
```
> 配合 [[Structured Output]] 与 [[Prompt 工程]] 使用。

### 2. 并发处理一批数据
```python
import asyncio, httpx

async def call_model(client, text):
    ...

async def main(texts):
    async with httpx.AsyncClient() as c:
        await asyncio.gather(*[call_model(c, t) for t in texts])
```

### 3. 接客户系统
```python
import httpx
r = httpx.get("https://client-api.example.com/orders",
              headers={"Authorization": f"Bearer {token}"})
```
> 涉及 [[OAuth]] / [[JWT]] 鉴权时注意 token 刷新。

---

## 五、常见坑

> [!warning] FDE 用 Python 的高频坑
> - **依赖管理混乱**：用 `venv` 或 `uv` 隔离，别污染全局环境；交付时用 [[Docker]] 固定版本。
> - **忘了异常处理**：接外部 API 必加 `try/except` + 重试（见 [[Debugging 与可观测性]]）。
> - **同步阻塞**：在 API 服务里写 `time.sleep` 或同步 HTTP，会拖垮整个服务。
> - **硬编码密钥**：密钥走环境变量，别写进代码（见 [[企业系统集成]] 安全部分）。

---

相关笔记：
- [[TypeScript]] —— 何时用 JS 生态而非 Python
- [[FastAPI]] —— Python 后端首选框架
- [[HTTP 客户端]] / [[pandas]] / [[asyncio]] / [[subprocess]] / [[Pydantic]] / [[SQLAlchemy]] / [[pytest]] —— Python 生态子工具
- [[FDE 学习路线]] —— Python 在第一阶段
