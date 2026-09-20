---
title: Structured Output
aliases: [结构化输出, JSON Mode, 结构化生成, Schema Output]
tags: [fde, ai, llm, output]
created: 2026-08-24
type: reference
domain: ai
layer: foundation
canonical: true
canonical_group: ai-structured-output
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://platform.openai.com/docs/overview]
---

# Structured Output

> [!abstract] 定位
> **Structured Output（结构化输出）** 让 LLM 返回 **程序可以直接消费** 的数据（通常是 JSON，符合预定义 schema）。对 FDE 而言，这是把「模型的文字」变成「系统的数据」的关键一步——没有它，AI 结果只能给人看，不能给流程用。

---

## 一、为什么它至关重要

FDE 的价值在于把 AI 焊进业务流程。流程需要的是字段，不是散文：

```text
模型输出（散文）        → 人能看，程序难用
模型输出（JSON）        → 直接写 [[PostgreSQL]]、推 [[Webhook]]、触发下一步
```

> [!note] 没有结构化，就没有自动化
> 一个只能「聊天」的 AI 是 Demo；一个能「吐出 `{category, priority, summary}`」的 AI 才能进生产。

---

## 二、三种实现方式

### 1. JSON Mode（最稳）
要求模型只输出合法 JSON：
```python
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[...],
)
```

### 2. 函数调用 / Tool Calling（更严）
把输出定义成「函数参数 schema」，模型填参（见 [[Tool Calling]]）。这是目前最可靠的方式。

### 3. 用 Pydantic 校验（兜底）
即使模型声称输出 JSON，也可能格式错。用 [[Python]] 的 Pydantic 二次校验：
```python
from pydantic import BaseModel, ValidationError
class Result(BaseModel):
    category: str
    priority: int
try:
    r = Result.model_validate(json.loads(raw))
except ValidationError:
    # 重试或降级
    ...
```

---

## 三、Schema 设计要点

- **字段越少越稳**：只取你真要用的。
- **给枚举**：`category` 用固定候选，别让模型自由发挥。
- **给示例值**：description 里写清楚每个字段含义与格式。
- **容错**：允许 `null` / 默认值，避免校验失败阻断流程。

```json
{
  "type": "object",
  "properties": {
    "category": {"type": "string", "enum": ["账单","理赔","投诉","其他"]},
    "priority": {"type": "integer", "minimum": 1, "maximum": 3},
    "summary": {"type": "string"}
  },
  "required": ["category", "priority"]
}
```

---

## 四、常见坑

> [!warning]
> - **迷信模型会守格式**：务必加校验 + 重试，否则偶发脏数据进库。
> - **schema 太复杂**：嵌套深、字段多 → 模型出错率飙升，拆小任务。
> - **把置信度当真理**：模型给的 `confidence` 不一定准，关键决策加人工/规则兜底。
> - **没处理解析失败**：JSON 解析异常要 catch，别让整个请求 500。

---

## 五、Schema 的演进与验收

- Schema 要有版本，新增可选字段优先，避免无通知删除或改类型。
- 解析成功不等于业务正确；继续做枚举、范围、权限和状态转换验证。
- 失败样例要进入回归集，区分模型格式错误、业务校验失败和下游写入失败。
- 对关键输出保留原始响应、解析结果、验证错误和最终处置，便于审计与回放。

相关笔记：
- [[LLM API]] —— 调用与成本
- [[Prompt 工程]] —— 用约束提升输出质量
- [[Tool Calling]] —— 更可靠的结构化入口
- Pydantic（见 [[Python]]）—— 校验落地
