---
title: REST API
aliases: [REST, RESTful, GraphQL, API 设计, 接口设计]
tags: [fde, backend, api, integration]
created: 2026-08-24
---

# REST API 与接口设计

> [!abstract] 定位
> **REST** 与 **GraphQL** 是 FDE 每天打交道的接口范式。FDE 的大量工作本质是「把不同系统连接起来」，所以理解 HTTP、REST、JSON、鉴权、限流、重试，比记住某个框架更重要。

> [!note] 重要澄清：REST 是「接口设计风格」，不是「后端框架」
> 常有人把 REST API 和 Django/FastAPI 并列叫「后端框架」——这是错的。REST 是**一套约定**（用 URL 表示资源、用 HTTP 动词表示操作、无状态、返回 JSON），不关心你用 Node.js、Python 还是 Go 实现；真正写服务的是其上的**框架**（FastAPI/Express）。三者的层次区分见 [[后端基础]] 的「三者不是一回事」，Node.js 的运行时定位见 [[Node.js]]。

---

## 一、REST 基础

REST 用 **资源 + HTTP 动词** 表达操作：

| 动词 | 含义 | 例子 |
| --- | --- | --- |
| GET | 读取 | `GET /tickets` |
| POST | 创建 | `POST /tickets` |
| PUT | 整体更新 | `PUT /tickets/1` |
| PATCH | 部分更新 | `PATCH /tickets/1` |
| DELETE | 删除 | `DELETE /tickets/1` |

配套概念：
- **Status Code**：`200` 成功、`201` 创建、`400` 参数错、`401/403` 鉴权、`429` 限流、`500` 服务端错。
- **Headers**：`Authorization`、`Content-Type`、`Accept`。
- **JSON**：事实上的数据交换格式。

---

## 二、GraphQL 是什么（何时用）

GraphQL 用 **一个端点 + 查询语句** 让客户端精确声明要哪些字段，避免 REST 的过度获取 / 多次往返。

```graphql
query {
  ticket(id: 1) {
    category
    priority
  }
}
```

> [!note] FDE 怎么选
> - 对接 **外部 SaaS / 客户系统**：它们大多只提供 REST（见 [[SaaS 集成]]、[[企业系统集成]]），跟着现成的来。
> - 自己做前端 + 复杂查询：GraphQL 可减少接口数量，但增加服务端复杂度。FDE 原型阶段通常先用 REST，跑通再优化。

---

## 三、FDE 必懂的「接口周边」

光会发请求不够，还要懂：

- **Authentication**：[[OAuth]]、[[JWT]]、API Key。
- **Rate Limit**：第三方常限流，需退避重试。
- **Timeout**：设合理超时，别让请求挂死。
- **Retry**：幂等接口才可安全重试（GET / 带幂等键的 POST）。
- **Pagination**：列表接口用 `cursor` 或 `offset` 翻页，别一次拉爆。
- **Webhook**：被动接收事件（见 [[Webhook]]），比轮询省资源。

---

## 四、调试接口的工具习惯

- `curl` / `httpie` 快速探接口（[[Linux]] 环境必备）。
- Postman / Insomnia 做集合与环境变量。
- 在 [[FastAPI]] 里自动生成的 `/docs` 直接试。

```bash
curl -X POST https://api.example.com/analyze \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"text":"退款工单"}'
```

---

## 五、常见坑

> [!warning]
> - **把 4xx 当 5xx 处理**：401 是鉴权问题，429 是限流，要不同策略。
> - **忽略幂等**：重试导致重复创建订单/工单。
> - **不分页拉全量**：数据一多就超时或内存爆。
> - **状态码乱用**：成功返回 200 但 body 里带 error，前端难处理。

---

相关笔记：
- [[FastAPI]] / [[Node.js]] —— 怎么实现 REST
- [[OAuth]] / [[JWT]] —— 鉴权
- [[Webhook]] —— 事件驱动补充
- [[企业系统集成]] —— 真实系统的连接
