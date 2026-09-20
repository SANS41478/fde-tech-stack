---
title: 生产就绪与上线 Runbook
aliases: [Production Readiness, 上线检查清单, 发布与回滚手册]
tags: [fde, infra, production, runbook, operations]
created: 2026-09-20
type: guide
domain: infra
layer: implementation
canonical: true
canonical_group: production-readiness
status: active
updated: 2026-09-20
reviewed: 2026-09-20
stability: evergreen
sources: [https://opentelemetry.io/docs/, https://sre.google/sre-book/service-level-objectives/, 本库综合整理]
---

# 生产就绪与上线 Runbook

## 一、上线前门禁

- [ ] 配置、密钥、域名、证书和环境变量已分离。
- [ ] 数据库迁移可前向执行，必要时可兼容旧版本。
- [ ] 备份已完成，恢复演练成功并记录耗时。
- [ ] 健康检查、结构化日志、Trace、指标和告警可用。
- [ ] 关键路径有单元、集成、E2E、权限和回归测试。
- [ ] 资源、连接池、队列、限流和成本预算已估算。
- [ ] 灰度比例、停止条件和回滚命令已写入 Runbook。
- [ ] 业务 owner、值班人和升级联系人已确认。

## 二、参考拓扑

```text
用户
 ↓
CDN / WAF / HTTPS
 ↓
Web / API
 ├─ Auth / Tenant / Rate Limit
 ├─ Queue → Worker → 外部 API / LLM
 ├─ PostgreSQL
 ├─ Redis
 └─ Object Storage
        ↓
   Logs / Metrics / Traces / Alerts
```

每条关键请求至少能通过 `request_id`、`trace_id`、`tenant_id`（脱敏）和 `release_id` 关联到日志、工具调用和结果。

## 三、发布步骤

1. 冻结发布版本、迁移版本和配置快照。
2. 在预发布环境执行迁移、冒烟、权限和回归任务。
3. 小比例灰度，观察错误率、p95 延迟、队列积压和业务成功率。
4. 达到验收阈值后逐步扩大流量。
5. 发布完成后保留旧版本、指标和审计记录，直到观察窗口结束。

## 四、回滚与事故处理

触发回滚的条件包括：关键任务失败、数据越权、重复写入、错误率持续超阈值、不可接受的成本或延迟。

回滚顺序：

1. 停止扩大流量，必要时关闭 Feature Flag 或高风险写操作。
2. 保留现场：日志、Trace、输入摘要、版本和配置。
3. 回退应用、Prompt、模型路由或工具策略。
4. 数据变更使用补偿迁移或恢复方案，不直接删除生产数据。
5. 验证关键路径、队列积压和外部系统状态。
6. 记录时间线、影响范围、根因、修复和预防动作。

## 五、日常运维检查

| 频率 | 检查 |
| --- | --- |
| 每次发布 | 冒烟、迁移、灰度、回滚路径 |
| 每日 | 错误率、p95、队列积压、成本、备份 |
| 每周 | 依赖漏洞、密钥轮换计划、死信和失败任务 |
| 每月 | 恢复演练、容量趋势、SLO 复盘和权限审计 |

相关笔记：[[System Design]]、[[Debugging 与可观测性]]、[[CI-CD]]、[[Docker]]、[[VPS 运维与 1Panel]]、[[PostgreSQL]]、[[托管数据库与 Drizzle]]
