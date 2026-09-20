---
title: 上线与回滚 Runbook
aliases: [Release Runbook, Deployment Checklist]
tags: [fde, template, release, operations]
created: 2026-09-20
type: guide
domain: engineering
layer: implementation
canonical: true
canonical_group: template-release-runbook
status: active
updated: 2026-09-20
reviewed: 2026-09-20
stability: evergreen
sources: [https://sre.google/sre-book/service-level-objectives/]
---

# 上线与回滚 Runbook

## 1. 发布信息

- 服务 / 功能：
- release_id：
- 负责人：
- 值班人：
- 影响租户：
- 变更窗口：

## 2. 上线前检查

- [ ] 代码、Prompt、模型、工具和配置版本已冻结
- [ ] 数据库迁移已在预发布验证
- [ ] 备份与恢复点已确认
- [ ] 监控、告警和健康检查可用
- [ ] 冒烟、权限、E2E 和回归测试通过
- [ ] 灰度比例与停止条件已写明

## 3. 发布步骤

1. 
2. 
3. 

## 4. 观察指标

- 错误率：
- p95 延迟：
- 队列积压：
- 业务成功率：
- 成本：
- 越权 / 敏感数据事件：

## 5. 回滚触发与操作

触发条件：

- 

回滚步骤：

1. 停止扩大流量或关闭 Feature Flag。
2. 保留日志、Trace、配置和版本证据。
3. 执行应用 / 数据 / Prompt / 模型路由回滚。
4. 验证关键路径和外部系统状态。
5. 通知业务 owner 并记录事故时间线。

## 6. 交接与复盘

- 已知限制：
- 未解决问题：
- 后续 owner：
- 复盘日期：
