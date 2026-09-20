---
title: Webhook
aliases: [webhook, 回调, 事件回调, 反向 API]
tags: [fde, automation, integration, api]
created: 2026-08-24
type: reference
domain: automation
layer: foundation
canonical: true
canonical_group: automation-webhook
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://spec.openapis.org/oas/latest.html]
---

# Webhook

> [!abstract] 定位
> **Webhook（回调）** 是「事件发生时，对方主动推消息给你」的机制。和 [[REST API]] 的「你去拉」相反，Webhook 是「它来推」。FDE 做系统集成时，Webhook 是接收客户系统实时事件的最省资源方式。

---

## 一、拉 vs 推

```text
轮询（Polling）：你每隔 N 秒调 API 问「有新数据吗？」→ 费资源、有延迟
Webhook（Push）：事件一发生，对方 POST 给你 → 实时、省资源
```

> [!note] 出现在两个板块
> Webhook 既在「自动化」也在「系统集成」里——因为它既是自动化触发器，也是系统连接手段。本篇为统一出处，两处都链接到这里。

---

## 二、FDE 典型用法

- 客户 CRM 新建工单 → Webhook 推给 FDE 服务 → 调 [[LLM API]] 分析 → 结果回写或推 Slack。
- 支付成功事件 → 触发后续业务流。
- GitHub / SaaS 事件 → 驱动 [[CI-CD|CI/CD]] 或通知。

```text
客户 CRM
   ↓ Webhook (POST JSON)
FDE Solution（[[FastAPI]] / [[Node.js]] 接收端）
   ↓
AI 分析
   ↓
CRM / Slack / Email
```

---

## 三、实现一个接收端

### FastAPI 示例
```python
@app.post("/webhook/crm")
async def crm_webhook(payload: dict):
    # 1. 校验签名（见下）
    # 2. 尽快返回 200（别在函数里做重活）
    # 3. 重活丢后台任务 / 队列（[[Redis]] / [[ETL 与数据管道]]）
    enqueue(payload)
    return {"status": "ok"}
```

### 关键注意
- **立刻回 200**：第三方通常要求快速响应，重处理异步做，否则会被判失败重发。
- **幂等**：同一事件可能重发，用事件 ID 去重。
- **签名校验**：验证 `X-Signature` 防伪造（用共享密钥 HMAC）。
- **限流 / 排队**：突发流量用 [[Redis]] 缓冲。

## 五、重放、防伪与死信

推荐把 Webhook 接收拆成三步：

1. 验证签名、时间戳和事件 ID，拒绝过期或重复请求。
2. 将原始 payload、来源、接收时间和签名结果写入不可变事件表，快速返回。
3. 异步消费，成功确认；失败按错误类型重试，超过阈值进入死信队列。

死信记录至少包含事件 ID、租户、来源、最后错误、重试次数和可安全重放的引用。修复消费者后优先在沙盒重放，再按批次恢复生产。

---

## 六、常见坑

> [!warning]
> - **在 Webhook 里做重活**：超时导致对方重试 → 重复处理，必须异步。
> - **不校验签名**：任何人都能伪造事件，安全风险。
> - **不处理重复**：重试机制下重复事件是常态，缺幂等就出脏数据。
> - **公网暴露无保护**：接收端要鉴权 + HTTPS，别裸奔。

---

相关笔记：
- [[REST API]] —— 拉取式对照
- [[Cron]] —— 定时触发对照
- [[事件驱动 Agent]] —— Webhook 是 Agent 外部事件通道的基础设施
- [[企业系统集成]] —— Webhook 是连接手段
- [[Redis]] —— 缓冲与去重
