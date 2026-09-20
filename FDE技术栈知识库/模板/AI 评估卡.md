---
title: AI 评估卡
aliases: [AI Eval Card, Agent Evaluation Card]
tags: [fde, template, ai, evaluation]
created: 2026-09-20
type: guide
domain: ai
layer: implementation
canonical: true
canonical_group: template-ai-eval-card
status: active
updated: 2026-09-20
reviewed: 2026-09-20
stability: moving
sources: [https://platform.openai.com/docs/guides/evals]
---

# AI 评估卡

## 1. 任务与风险

- Agent / 功能：
- 业务目标：
- 用户与租户：
- 高风险动作：
- 明确不允许的行为：

## 2. 数据集

- 任务来源：
- 正常集：
- 边界集：
- 保留集：
- 对抗集：
- 脱敏与授权：

## 3. 指标与门槛

| 指标 | 定义 | 目标 | 护栏 |
| --- | --- | --- | --- |
| 任务成功率 |  |  |  |
| 关键错误率 |  |  |  |
| Pass^k |  |  |  |
| p95 延迟 |  |  |  |
| 单任务成本 |  |  |  |
| 越权/泄露 |  |  |  |

## 4. 评估配置

- 模型与版本：
- Prompt 版本：
- 工具 Schema 版本：
- 检索器 / 索引版本：
- 温度、最大步数和预算：
- 验证器：

## 5. 发布决定

- [ ] 边界集达到目标
- [ ] 保留集无关键回归
- [ ] 高风险动作有审批
- [ ] 轨迹可审计和重放
- [ ] 灰度、监控和回滚已准备
- 发布结论：
