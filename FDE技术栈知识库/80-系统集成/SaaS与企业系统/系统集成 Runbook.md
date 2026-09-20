---
title: 系统集成 Runbook
aliases: [连接器 Runbook, 集成上线手册, Integration Runbook]
tags: [fde, integration, runbook, reliability]
created: 2026-09-20
type: guide
domain: integration
layer: implementation
canonical: true
canonical_group: integration-runbook
status: active
updated: 2026-09-20
reviewed: 2026-09-20
stability: evergreen
sources: [https://spec.openapis.org/oas/latest.html, 本库综合整理]
---

# 系统集成 Runbook

## 一、集成前置条件

- [ ] 业务 owner、系统 owner、数据 owner 和安全审批人已确认。
- [ ] 沙盒与生产环境、租户、账号、权限和凭证用途已区分。
- [ ] 字段映射、时间格式、时区、枚举、空值和删除语义已确认。
- [ ] API 文档、示例响应、分页、限流、Webhook 签名和错误码已留档。
- [ ] 写操作的幂等键、撤销方式和人工审批边界已定义。

## 二、集成契约最小内容

```yaml
connector:
  owner: integration-team
  source_system: crm
  target_system: case-platform
  sync_mode: webhook_plus_cursor
  idempotency_key: source_event_id
  retryable_errors: [408, 409, 429, 500, 502, 503, 504]
  dead_letter_after: 5
  replay_from: cursor
  pii_fields: [email, phone]
```

契约必须说明：谁拥有字段、何时更新、冲突谁胜出、失败如何重试、重复如何去重、删除是否传播，以及怎样回放一段时间的数据。

## 三、运行时闭环

```text
接收事件/轮询
  → 验签与权限检查
  → 规范化与幂等去重
  → 入队并记录游标
  → 处理与写入
  → 验证目标状态
  → 成功确认 / 失败进入重试或死信
```

重试规则：

- 只重试明确可恢复的错误，指数退避并加入抖动。
- 不可重试错误进入人工处理，不要原样重复调用。
- 外部系统返回 429 时尊重 `Retry-After`。
- 每次尝试记录 connector、事件 ID、租户、版本、耗时和错误分类。

## 四、补数、重放与回滚

1. 先冻结影响范围和时间窗口。
2. 从原始事件、源系统游标或不可变日志生成待处理清单。
3. 在沙盒重放，验证重复、顺序、删除和权限行为。
4. 生产小批量执行，观察错误率、延迟和目标系统写入量。
5. 发现异常立即停止新批次，保留已处理记录，按幂等键安全重跑。

> [!warning] 不要直接“清空后重灌”
> 破坏性清理可能删除客户在同步期间手工修正的数据。优先使用版本标记、补偿事务、隔离批次和可审计回滚。

## 五、验收与故障归属

验收至少覆盖：

- 正常创建、更新、删除和重复事件。
- 429、超时、断网、权限不足、无效字段和目标系统 5xx。
- Webhook 签名错误、重放攻击和乱序事件。
- 跨租户访问、PII 脱敏、日志审计和凭证轮换。
- 回放、补数、停机恢复和版本升级。

故障归属按证据判断：

| 现象 | 优先检查 |
| --- | --- |
| 没有收到事件 | 源系统投递、签名、网络和入口日志 |
| 收到但未处理 | 队列、去重表、解析器和权限 |
| 重复写入 | 幂等键、事务边界和重试策略 |
| 数据延迟 | 限流、队列积压、下游响应和 Worker |
| 结果错误 | 字段映射、版本兼容和业务规则 |

相关笔记：[[企业系统集成]]、[[SaaS 集成]]、[[Webhook]]、[[REST API]]、[[API 产品化]]、[[认证与授权机制]]
