---
title: Pydantic
aliases: [Pydantic, pydantic, 数据校验, 配置管理]
tags: [fde, python, validation, schema]
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

# Pydantic（数据校验 / 配置）

> [!abstract] 定位
> **Pydantic** 用 Python 类型注解定义 **数据模型**，在运行时自动校验、转换、报错。它是 FDE 保证「进来的数据是对的、出去的数据是结构化的」的基石——既服务于 [[FastAPI]] 的接口校验，也服务于把 [[LLM API]] 的胡乱输出收敛成可用结构（[[Structured Output]]）。

---

## 一、为什么 FDE 要会

- **接口契约**：[[FastAPI]] 用 Pydantic 定义请求/响应模型，脏数据在入口就被挡下。
- **LLM 输出落地**：模型返回的 JSON 用 Pydantic 校验，缺字段/类型错立刻发现（配合 [[Structured Output]]）。
- **配置管理**：用 `BaseSettings` 从环境变量读配置（密钥、连接串），不硬编码（见 [[企业系统集成]] 安全）。
- **数据管道中间结构**：[[ETL 与数据管道]] 中每段输入输出都有模型约束，易维护。

---

## 二、核心用法

```python
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    id: int
    category: str = Field(..., min_length=1)   # 必填且有约束
    priority: int = Field(default=3, ge=1, le=5)
    tags: list[str] = []

# 校验 + 自动类型转换
t = Ticket(id="123", category="billing")   # id 自动转 int
print(t.model_dump())                       # 转 dict
print(t.model_dump_json())                  # 转 JSON
```

### 与 FastAPI 配合
```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/tickets")
def create(t: Ticket):        # 请求体自动校验
    return {"ok": True, "id": t.id}
```

### 与 LLM 配合（结构化输出校验）
```python
# 模型返回 JSON → 用 Ticket 校验，确保字段齐全、类型正确
parsed = Ticket.model_validate(llm_json)
```

---

## 三、FDE 实战要点

- **在边界校验**：API 入口、LLM 输出、外部数据落地处都用模型挡一道。
- **明确必填与默认**：用 `Field` 表达约束（范围、长度），而不是散落在代码里的 `if`。
- **错误要可读**：校验失败的 `ValidationError` 可直接转成给客户的友好提示。
- **配置集中**：用 Settings 类统一读环境变量，配合 [[Docker]] / [[Docker Compose]] 的 `.env`。

---

## 四、常见坑

> [!warning]
> - **v1 / v2 差异**：API 不同（如 `parse_obj` vs `model_validate`），团队要统一版本。
> - **过度宽松 coerce**：Pydantic 会做隐式转换（如 `"123"`→`123`），有时掩盖脏数据，关键处用严格模式 `model_config = ConfigDict(strict=True)`。
> - **嵌套模型不校验**：深层嵌套要确认都定义了模型，别用 `dict` 逃避。
> - **大额/精度**：默认 float 有精度问题，金额用 `Decimal` 或字符串。
> - **配置类进了版本库**：含密钥的 `.env` 必须 `.gitignore`（见 [[Git]]）。

---

相关笔记：
- [[Python]] —— 所属语言
- [[FastAPI]] —— 原生集成
- [[Structured Output]] —— LLM 输出校验落地
- [[LLM API]] —— 被校验的来源
- [[Docker Compose]] —— 配置通过 .env 注入
