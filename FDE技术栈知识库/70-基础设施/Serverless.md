---
title: Serverless
aliases: [FaaS, 函数即服务, 无服务器, Lambda, Cloud Functions]
tags: [fde, infra, devops, serverless]
created: 2026-08-27
type: reference
domain: infra
layer: foundation
canonical: false
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://opentelemetry.io/docs/]
---

# Serverless / FaaS

> [!abstract] 定位
> **Serverless（FaaS，函数即服务）** 是 [[云服务模型]] 里最上层一档：你只写一个个函数，平时没机器在跑（不花钱），有请求 / 事件来了平台临时起容器执行、跑完回收。常被人误以为「只是云上小工具、没场景」——本文列真实用法。与 [[部署方式]] 的 Serverless 段互补。

---

## 一、和 PaaS / 常驻 VM 的区别

- **常驻 VM / 容器**：机器 24h 开着，哪怕一天只干 5 秒活，你也付 24h 的钱。
- **PaaS**：平台常驻托管你的服务，按运行时间 / 实例计费。
- **FaaS**：按**调用次数 + 执行时长**计费，空闲零成本。

> [!tip] 误区的根源
> 「功能简单就没必要部署」错在把成本当成「功能复杂度」，其实是「养一台机器」。一个每天跑 5 秒的任务，用 VM 付全天钱，用 FaaS 只付那 5 秒。

---

## 二、真实应用场景

- **事件驱动**：文件传进 S3 → 自动触发函数做转码 / 缩略图；数据库变更 → 触发通知。
- **Webhook 处理**：接收支付回调、GitHub 推送事件（见 [[Webhook]]）。
- **定时任务（cron）**：每天凌晨汇总数据、清理过期记录（见 [[Cron]]）。
- **突发 / 低流量后端**：配 API 网关做轻量 API，平时 0 成本，流量来了才计费。
- **流式数据处理**：日志实时过滤、转发。

---

## 三、不适合的场景

- 长时间运行（> 平台超时，通常分钟级）。
- 对冷启动延迟敏感（首次调用要现起容器，几十~几百 ms）。
- 需要常驻内存状态 / 特殊硬件 / 底层系统权限。

---

## 四、FDE 视角

- 做客户集成时，用 FaaS 处理**偶发事件**最划算（如「客户系统推一条消息就转发到 Slack」），不用为此养服务。
- 配合 [[静态托管与边缘]] 的前端，后端轻逻辑可直接用 Cloud Functions / Lambda，整体接近零运维。

---

相关笔记：
- [[云服务模型]] —— FaaS 在责任谱的最上层
- [[部署方式]] —— Serverless 形态的对比
- [[Webhook]] —— 典型触发源
- [[Cron]] —— 定时触发
- [[静态托管与边缘]] —— 前端 + FaaS 组合
- [[云平台]] —— AWS Lambda / GCP Cloud Functions
