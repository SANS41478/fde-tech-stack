---
title: AI 应用生产化
aliases: [AI Application Production, LLM 应用上线, AI 生产系统]
tags: [fde, ai, production, reliability, evaluation]
created: 2026-09-20
type: guide
domain: ai
layer: implementation
canonical: true
canonical_group: ai-production
status: active
updated: 2026-09-20
reviewed: 2026-09-20
stability: moving
sources: [https://platform.openai.com/docs/guides/production-best-practices, https://opentelemetry.io/docs/, 本库综合整理]
---

# AI 应用生产化

> [!abstract] 核心
> 生产 AI 系统不是“接上模型 API”。它必须同时具备可控输入、可验证输出、受限工具、可观测轨迹、成本边界、降级路径和可回滚版本。

## 一、从模型调用到产品闭环

```text
用户请求
  → 身份/租户/数据权限
  → Prompt + 当前状态 + 检索证据
  → 模型路由与预算
  → 结构化输出 / 工具调用
  → 确定性验证器
  → 执行、人工审批或拒绝
  → Trace、指标、反馈与评估集
```

## 二、版本化边界

以下内容必须可追踪、可比较、可回滚：

- 模型与供应商版本。
- 系统 Prompt、工具 Schema、输出 Schema。
- RAG 索引版本、检索器配置和权限过滤规则。
- 评估集、Rubric、验证器和安全策略。
- 路由、超时、重试、成本预算和 Feature Flag。

一次发布应生成一个不可变的运行配置，例如：

```yaml
release: ai-assistant-2026-09-20.1
model: primary-model@version
prompt: support-v14
retriever: hybrid-v3
tool_policy: approval-v5
eval_gate:
  pass_rate: ">= 0.90"
  critical_failures: 0
  p95_latency_ms: "<= 8000"
  cost_per_task: "<= 0.05"
```

## 三、模型路由与降级

- 简单分类、抽取和改写优先使用低成本模型。
- 高风险、高歧义或复杂工具规划才升级到强模型。
- 备用模型必须先经过同一输出 Schema、权限和回归测试。
- 超时、429、供应商故障和格式错误应有不同恢复策略。
- 重试必须受预算与熔断器限制，不能把低成功率模型“重试到成功”。

## 四、RAG 与 Agent 的生产门槛

RAG 上线前必须验证：

- 召回率、重排质量、引用正确性和数据新鲜度。
- 租户/角色/文档 ACL 在检索前后都生效。
- 文档删除、权限变更和索引延迟有明确行为。
- 未找到证据时能拒答或转人工，不编造来源。

Agent 上线前必须验证：

- 工具参数、权限、幂等、超时和取消语义。
- 高风险工具需要确认或独立审查。
- 边界集改善、保留集不退化。
- 轨迹可重放，失败能定位到首次错误。
- 连续失败、死循环和工具调用洪泛会自动熔断。

## 五、成本、延迟与安全指标

| 类别 | 最小指标 |
| --- | --- |
| 质量 | 任务成功率、关键错误率、引用准确率、误拒绝率 |
| 可靠性 | Pass^k、工具成功率、重试率、熔断次数 |
| 性能 | TTFT、p95 总延迟、队列等待、吞吐 |
| 成本 | 每任务输入/输出 token、缓存命中率、供应商费用 |
| 安全 | 越权率、注入拦截率、敏感数据泄露、人工升级率 |

## 六、上线与复盘

使用灰度或 Feature Flag 发布，先观察：

- 关键任务成功率与保留集回归。
- 高风险动作、人工审批和拒绝边界。
- 真实用户反馈、成本和 p95 延迟。
- 供应商错误、限流和上下文溢出。

任何新版本都必须能回到上一份 Prompt、工具策略、索引和模型配置。

相关笔记：[[LLM API]]、[[Prompt 工程]]、[[Structured Output]]、[[Tool Calling]]、[[RAG]]、[[Agent]]、[[Harness 工程]]、[[Agent 评估]]、[[提示注入]]
