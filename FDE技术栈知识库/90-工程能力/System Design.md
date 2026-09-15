---
title: System Design
aliases: [系统设计, 架构设计, System Architecture, 系统设计能力]
tags: [fde, engineering, design, architecture]
created: 2026-08-24
type: reference
domain: engineering
layer: foundation
canonical: true
canonical_group: engineering-system-design
status: active
updated: 2026-09-15
sources: []
---

# System Design（系统设计）

> [!abstract] 定位
> FDE 不必达到资深架构师水平，但应具备 **基本系统设计能力**：面对「每天处理 100 万条客户数据再用 AI 分析」这类需求，能画出可行架构，并权衡成本、延迟、可靠性。

---

## 一、FDE 视角的系统设计

普通研发做系统设计追求「高并发极致优化」；FDE 做系统设计追求 **「在不确定中快速给出能跑、能扩、能交付的方案」**。

典型场景思考：
> “每天处理 100 万条客户数据，然后用 AI 分析。”

```text
Data Source
     ↓
Queue（缓冲，见 [[Redis]]）
     ↓
Worker（并发处理，[[Python]] asyncio）
     ↓
LLM（[[LLM API]] 批量 / 异步）
     ↓
Database（[[PostgreSQL]]）
     ↓
Result → Dashboard
```

---

## 二、必须纳入考量的维度

```text
并发        # 多少同时跑？Worker 数？
成本        # 模型调用费、云资源费（见 [[LLM API]]、[[云平台]]）
延迟        # 用户等多久？流式？批处理？
可靠性      # 失败重试、幂等、降级
缓存        # [[Redis]] 减负
重试        # 指数退避，防雪崩
限流        # 保护下游，也被上游限流
安全        # 鉴权、权限、数据脱敏（见 [[OAuth]]、[[企业系统集成]]）
权限        # 谁能看什么数据
扩展性      # 数据量 ×10 还能跑吗？
```

---

## 三、FDE 常用的设计积木

- **Queue + Worker**：削峰填谷，异步处理（[[ETL 与数据管道]]、[[Redis]]）。
- **缓存层**：热点数据少查库（[[Redis]]）。
- **读写分离 / 批处理**：降成本提吞吐。
- **幂等设计**：重试安全，靠唯一键 / 去重（[[Webhook]]、[[REST API]]）。
- **降级与兜底**：模型/外部挂了，系统还能给基础结果。

---

## 四、如何锻炼

- 拿真实模糊需求，先画 **数据流图**（数据从哪来、到哪去、在哪被处理）。
- 对每个环节问：「这里会挂吗？慢吗？贵吗？」
- 用 [[FDE 练习项目]] 把设计落地成能跑的系统。
- 上线后靠 [[Debugging 与可观测性]] 验证假设。

---

## 五、常见坑

> [!warning]
> - **过度设计**：为「未来可能的百万 QPS」提前上重型架构，拖慢交付。先跑通，再按需演进。
> - **忽视成本**：无脑调最强模型 / 全量嵌入，账单爆炸。
> - **单点无冗余**：关键服务挂了全停，至少加重试与降级。
> - **不考虑幂等**：重试引入重复，数据错乱。

---

相关笔记：
- [[ETL 与数据管道]] —— Queue/Worker 落地
- [[Redis]] —— 缓存/队列
- [[LLM API]] —— 成本与可靠性
- [[Debugging 与可观测性]] —— 设计要可验证
- [[FDE 能力模型]] —— 系统设计属于技术能力
