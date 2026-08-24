---
title: SaaS 集成
aliases: [SaaS 集成, SaaS Integration, 第三方应用集成, 云服务集成]
tags: [fde, integration, saas]
created: 2026-08-24
---

# SaaS 集成

> [!abstract] 定位
> **SaaS 集成** 是把客户的 SaaS 应用（Salesforce、HubSpot、Slack、Jira、Notion、Google Workspace、Microsoft 365 等）与你的 FDE 方案连接起来的能力。这是 FDE「把 AI 焊进客户工作流」的最常见落点。

---

## 一、为什么 SaaS 集成是 FDE 核心

客户的业务数据和工作流大多活在 SaaS 里。FDE 的价值不是另起炉灶，而是：
> **让 AI 能力直接进客户已经在用的工具**——在 Slack 里问答、在 CRM 里自动补字段、在 Notion 里生成文档。

---

## 二、常见 SaaS 与集成点

```text
Salesforce / HubSpot   # CRM：客户/订单数据
Slack / 飞书 / 企微     # 通知 / 对话入口
Jira / Trello          # 工单 / 任务
Notion / 腾讯文档       # 知识 / 文档生成
Google Workspace / M365 # 邮件 / 日历 / 文档
ERP                    # 财务 / 供应链
```

集成手段通常是：[[REST API]] + [[OAuth]] 授权 + [[Webhook]] 事件 + [[JWT]] 鉴权。

---

## 三、典型场景

```text
客户 CRM
   ↓ API（[[OAuth]] Token）
FDE Solution
   ↓ [[LLM API]] 分析
结果 → CRM 回填 / Slack 通知 / Email
```

例如：每天把新增工单用模型分类优先级，自动写回 CRM 字段并 @ 负责人到 Slack。

---

## 四、FDE 实战要点

- **先读官方 API 文档**：每个 SaaS 的鉴权、分页、限流都不同。
- **用官方 SDK**：很多提供 [[TypeScript]] / [[Python]] SDK，省去手写 HTTP。
- **处理限流**：SaaS API 常严格限流，退避重试（见 [[REST API]]）。
- **事件驱动**：能用 [[Webhook]] 就别轮询，实时又省额度。
- **权限申请**：OAuth Scope 按最小需要申请，过客户安全审查。

---

## 五、常见坑

> [!warning]
> - **忽略 API 限流**：批量同步把配额打爆，被临时封禁。
> - **Webhook 不校验签名**：伪造事件注入脏数据（见 [[Webhook]]）。
> - **数据写回无幂等**：重复事件导致重复记录。
> - **Scope 不足反复改**：上线前没确认权限，中途要客户重新授权，拖进度。

---

相关笔记：
- [[企业系统集成]] —— SaaS 与内部系统的总览
- [[OAuth]] / [[JWT]] —— 鉴权
- [[REST API]] / [[Webhook]] —— 连接手段
- [[FDE 练习项目]] —— AI CRM 助手项目
