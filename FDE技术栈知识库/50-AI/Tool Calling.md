---
title: Tool Calling
aliases: [Function Calling, 工具调用, 函数调用, 模型调工具]
tags: [fde, ai, llm, agent]
created: 2026-08-24
---

# Tool Calling

> [!abstract] 定位
> **Tool Calling（工具调用）** 让 LLM 不只是「说话」，而是能 **决定调用哪个外部函数、传什么参数**，从而查数据库、调 API、读文件、操作浏览器。它是从「聊天机器人」走向 [[Agent]] 的枢纽。

---

## 一、它解决了什么

没有工具调用，模型只能基于训练知识回答，无法：
- 查实时数据（今天的订单？）
- 执行动作（发邮件、写库）
- 接入私有系统（客户 [[CRM]]）

Tool Calling 让模型输出「我要调 `get_orders(date)` 参数是今天」，由你的代码真正执行，再把结果喂回模型。

---

## 二、工作机制

```text
User: 今天有多少待处理工单？
  ↓
LLM 看到 tools 定义，决定调用 get_open_tickets()
  ↓ 输出 tool_call {name, arguments}
你的代码执行函数 → 返回结果
  ↓ 结果作为 tool 消息回传
LLM 基于真实数据生成最终回答
```

### 代码示例（OpenAI 风格）
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_open_tickets",
        "description": "查询指定日期的待处理工单数量",
        "parameters": {
            "type": "object",
            "properties": {"date": {"type": "string"}},
            "required": ["date"],
        },
    },
}]
resp = client.chat.completions.create(
    model="gpt-4o", messages=msgs, tools=tools)
# 若 resp.choices[0].message.tool_calls 非空 → 执行并回传
```

---

## 三、FDE 常见工具类型

- **查询类**：查 [[PostgreSQL]]、查 [[REST API]]（客户系统）
- **动作类**：发 [[Webhook]]、写库、调 SaaS（[[SaaS 集成]]）
- **计算类**：跑脚本、算指标
- **检索类**：触发 [[RAG]] 检索
- **浏览器类**：[[Playwright]] 操作网页

> [!tip] 和 [[Structured Output]] 的关系
> Tool Calling 本质是把「输出」定义成函数参数 schema，因此比纯 JSON 更可靠，是结构化输出的升级形态。

---

## 四、设计好工具的要点

- **描述清晰**：`description` 写清何时用、参数是啥，模型靠它选工具。
- **参数简单**：别让模型填复杂嵌套，降低出错。
- **幂等**：工具可能被重试，写操作要安全。
- **失败可恢复**：工具报错要返回可读信息，让模型自我纠正。

> [!tip] 深入：ACI 与工具生态
> 工具设计已演化为一门系统的工程学科（ACI，Agent-Computer Interface）：专用工具 vs Skill + 通用执行器的选择、粒度权衡、参数传递保真性、Sidecar 安全审查、主动工具发现等——详见 [[工具设计原则]]。工具太多时的延迟加载与语义检索方案也在其中。

---

## 五、常见坑

> [!warning]
> - **工具太多让模型选晕**：只暴露当前任务相关工具。
> - **工具执行没超时**：一个慢工具卡死整个循环。
> - **把危险操作直接暴露**：删库、发钱类工具要加确认/权限（见 [[企业系统集成]] 安全）。
> - **不把结果回传**：调了工具忘了把结果喂回模型，它继续瞎编。

---

相关笔记：
- [[Structured Output]] —— 更基础的结构化
- [[Agent]] —— 工具调用组成的循环
- [[MCP]] —— 工具调用的标准化协议
- [[工具设计原则]] —— ACI / 粒度 / Sidecar / 主动发现
- [[Agent Skills]] —— Skill + 通用执行器路线
- [[RAG]] / [[Playwright]] —— 典型工具实现
