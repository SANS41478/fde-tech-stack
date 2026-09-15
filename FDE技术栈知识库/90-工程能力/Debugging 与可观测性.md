---
title: Debugging 与可观测性
aliases: [Debugging, 可观测性, Observability, 排错, 日志监控]
tags: [fde, engineering, debugging, observability]
created: 2026-08-24
type: reference
domain: engineering
layer: foundation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# Debugging 与可观测性

> [!abstract] 定位
> 优秀 FDE 与普通 Demo 开发者的重要分水岭之一，是 **出了问题能快速定位**。可观测性（Logs / Metrics / Tracing）让你在客户现场不靠猜，而是靠证据定位。

> [!quote] 核心
> 出了问题以后能够快速定位——这比「代码写得多漂亮」更决定客户信任。

---

## 一、三大支柱

```text
Logs        # 日志：发生了什么（文字记录）
Metrics     # 指标：量化状态（QPS、延迟、错误率）
Tracing     # 追踪：一次请求穿越哪些服务/层
```

辅助概念：Error Tracking（错误聚合）、Performance（性能）、Latency（延迟）、Timeout（超时）、Retry（重试）、Rate Limit（限流）。

---

## 二、FDE 的排查思路（通用）

```text
问题出现
  ↓ 复现（能复现才修得动）
定位 Layer（前端 / 后端 / DB / 模型 / 外部 API）
  ↓ 查看 Logs
确认输入（请求参数对吗）
  ↓ 确认 API（第三方返回什么）
确认数据库（数据对吗）
  ↓ 确认模型（prompt / token / 输出）
修复 → 验证（复现路径再走一遍）
```

> [!tip] 分层定位
> 别一上来改代码。先判断问题在哪一层：是 [[Next.js]] 前端没传参？[[FastAPI]] 报错？[[PostgreSQL]] 慢？[[LLM API]] 抽风？还是客户 [[REST API]] 限流？

---

## 三、FDE 实战工具

- **日志**：应用打结构化日志（JSON），用 `docker compose logs -f` 或云日志（见 [[Docker Compose]]、[[云平台]]）。
- **命令行排查**：[[Linux]] 的 `tail -f`、`curl` 探接口。
- **错误追踪**：Sentry 等聚合异常。
- **关键路径埋点**：模型调用耗时、外部 API 耗时单独记，方便发现瓶颈。

---

## 四、FDE 特别要观测的 AI 层

- **Token 用量**：监控成本，防跑飞（见 [[LLM API]]）。
- **模型错误率**：解析失败 / 校验失败比例（[[Structured Output]]）。
- **工具调用失败**：Agent 调工具超时/报错（[[Tool Calling]]、[[Agent]]）。
- **检索质量**：RAG 召回是否相关（[[RAG]]）。

---

## 五、常见坑

> [!warning]
> - **没日志**：出问题全靠脑补，现场尬住。
> - **日志打满敏感数据**：合规风险，脱敏。
> - **只测 happy path**：异常分支没覆盖，生产才爆。
> - **不监控线上**：服务挂了几小时才发现，客户先发现。
> - **重试无退避**：雪崩式请求把下游打挂。

---

## 六、Agent 可观测性（进阶）

Agent 系统把可观测性变得更难：同样的输入可能产生不同输出、多轮推理路径复杂、模型"思考"不透明。Agent 侧的数据结构与工具链：

- **Trace / Span 树**：每次任务一条 trace；LLM 调用、工具调用、检索各是一个 span（输入输出、起止时间、token 消耗、错误），父子关系构成执行树。协议标准：OpenTelemetry + OpenInference（LLM 语义约定）。
- **平台**：LangSmith / Langfuse / Arize Phoenix——A/B 测试、提示词版本管理、轨迹回放。
- **闭环**：生产轨迹筛失败案例 → 脱敏 → 沉淀为评估集新用例——评估集成为活资产（见 [[Agent 评估]]）。
- **成本监控**：按任务类型/模型/用户追踪 token 与 API 费用；单任务成本上限防跑飞。

---

相关笔记：
- [[Linux]] —— 命令行排错主战场
- [[Git]] —— 出问题回滚
- [[CI-CD|CI/CD]] —— 上线与回滚
- [[Agent 评估]] —— Trace 树、评估闭环与回归任务
- [[System Design]] —— 在设计阶段就考虑可靠性
