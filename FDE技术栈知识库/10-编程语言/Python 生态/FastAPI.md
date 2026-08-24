---
title: FastAPI
aliases: [fastapi, Fast API, Python Web 框架]
tags: [fde, backend, python, api]
created: 2026-08-24
---

# FastAPI

> [!abstract] 定位
> **FastAPI** 是基于 Python 类型注解的异步 Web 框架。对 AI FDE 来说，它是后端服务的首选：开发速度快、API 简单、与 Python AI 生态无缝衔接、非常适合快速原型。

---

## 一、为什么 FDE 选 FastAPI 而非 Django/Flask

| 维度 | Flask | Django | FastAPI |
| --- | --- | --- | --- |
| 上手速度 | 快 | 中（约定多） | 快 |
| 异步支持 | 需扩展 | 部分 | 原生（async/await） |
| 类型校验 | 无 | 部分 | 原生（Pydantic） |
| AI 生态契合 | 一般 | 一般 | 极佳 |
| 自动文档 | 无 | 插件 | 自动（Swagger） |

> [!tip] FDE 的判据
> 调 [[LLM API]] 时经常要 **高并发异步** + **结构化输入输出校验**，FastAPI 原生满足这两点，且写完自动有可交互 API 文档，给客户/同事调试极方便。

---

## 二、典型架构位置

```text
Frontend ([[Next.js]] / [[React]])
   ↓ HTTP / [[REST API]]
FastAPI
   ↓
Business Logic
   ↓
LLM / [[PostgreSQL]] / External API
```

---

## 三、最小可用示例

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/analyze")
async def analyze(q: Query):
    # 调 LLM、查 DB、调外部 API ...
    return {"result": f"分析了: {q.text}"}
```
启动：`uvicorn main:app --reload`，访问 `/docs` 即见 Swagger。

---

## 四、FDE 必会能力

### 1. 路径 / 查询 / 请求体
- `@app.get("/items/{id}")` 路径参数
- `?page=1` 查询参数
- `BaseModel` 请求体（自动校验）

### 2. 依赖注入（Dependencies）
用于鉴权（[[OAuth]] / [[JWT]]）、数据库连接共享。

### 3. 后台任务 / 流式
- 长任务用 `BackgroundTasks` 或任务队列（见 [[ETL 与数据管道]] 的 Worker 思路）。
- 流式响应用 `StreamingResponse` 配合 [[LLM API]] 的 token 流。

### 4. CORS
前端跨域调用必须配置：
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```

### 5. 容器化
几乎总是配合 [[Docker]] 部署，见 [[Docker Compose]] 多服务编排。

---

## 五、常见坑

> [!warning]
> - **在 async 函数里写同步阻塞代码**（如 `requests.get`、`time.sleep`）：会卡死事件循环，改用 `httpx.AsyncClient`。
> - **把密钥硬编码**：走环境变量 / `.env`（不进仓库）。
> - **没做输入校验**：依赖 Pydantic 挡住脏数据。
> - **忘了异常处理**：外部 API 失败要有兜底，见 [[Debugging 与可观测性]]。

---

相关笔记：
- [[Python]] —— FastAPI 的运行语言
- [[REST API]] —— 接口设计基础
- Pydantic（见 [[Python]] 技术栈）→ [[Structured Output]]
- [[Docker]] / [[Docker Compose]] —— 部署
- [[FDE 学习路线]] —— 第一阶段后端
