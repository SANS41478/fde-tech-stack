---
title: Web 测试与 E2E
aliases: [API 测试, E2E 测试, 端到端测试, Flaky Test, TDD]
tags: [fde, engineering, testing, e2e, playwright]
created: 2026-09-14
type: reference
domain: engineering
layer: foundation
canonical: true
canonical_group: engineering-web-test
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: evergreen
sources: [https://opentelemetry.io/docs/]
---

# Web 测试与 E2E

> [!abstract] 定位
> [[pytest]] 讲 Python 单元测试，[[Playwright]] 讲浏览器自动化；本篇把 API、页面、Git Hooks 和 CI 串成 Web 产品的测试闭环。

## 一、测试金字塔

```text
        E2E：少量关键用户旅程
      集成：API + 数据库 + 外部服务
    单元：大量、快速、定位明确
```

- 单元测试保护纯逻辑。
- API / 集成测试保护契约、校验、权限和数据库行为。
- E2E 测试保护「用户从页面完成任务」的关键路径。

不要把所有场景都写成 E2E；运行慢、失败难定位、维护成本高。

## 二、API 测试四类场景

每个重要接口至少覆盖：

1. 正常输入和正常响应。
2. 缺字段、类型错误、非法值。
3. 未登录、无权限、跨租户访问。
4. 空数据、重复提交、超时、限流和边界大小。

```text
Given 已登录但不是该组织成员
When 请求 GET /projects/other-org
Then 返回 403，且不泄露资源是否存在
```

测试应断言状态码、响应 Schema、数据库副作用和错误码，而不是只断言「请求没报错」。

## 三、Playwright E2E 最小结构

```text
tests/
├── auth.setup.ts
├── smoke/
│   ├── login.spec.ts
│   └── create-ticket.spec.ts
└── fixtures/
```

关键原则：

- 用稳定的角色或 `data-testid` 定位，不依赖脆弱 CSS。
- 测试前准备数据，测试后清理数据。
- 复用认证状态，避免每个用例重复登录。
- 断言用户能看到的结果和关键网络响应。
- 对外部支付、邮件、第三方 API 使用 Mock 或沙盒。

## 四、Flaky Test 排查

常见原因：

- 固定 `sleep`，没有等待真实状态。
- 测试共享数据库或账号。
- 依赖外部服务、时间、随机数。
- 选择器匹配多个元素。
- 并行测试互相污染。
- 页面存在动画或异步请求未完成。

排查顺序：

```text
保存失败截图 / 视频 / Trace
  ↓
确认失败发生在哪一步
  ↓
检查网络请求和服务端日志
  ↓
消除时间、随机数和数据共享依赖
  ↓
单独重跑并加入回归
```

不要通过「重试十次直到过」掩盖真正的不稳定。

## 五、Git Hooks 与 CI

提交前适合执行快速检查：

```text
格式化 → 类型检查 → Lint → 单元测试
```

推送或 PR 时执行：

```text
安装依赖 → 构建 → API 测试 → 关键 E2E → 安全扫描
```

把完整测试放 CI，不要让本地 Hook 成为唯一质量门槛。详见 [[CI-CD|CI/CD]]。

## 六、TDD 的轻量用法

```text
先写一个失败的验收条件
  ↓
实现最小代码
  ↓
运行测试
  ↓
重构
```

FDE 不需要所有功能都严格 TDD；对支付、权限、数据迁移、核心业务规则和历史 Bug，优先补测试保护。

## 七、上线前检查

- [ ] 关键 API 覆盖正常、校验、权限、边界场景。
- [ ] 关键用户旅程至少有一条 E2E。
- [ ] E2E 不依赖固定等待和个人账号。
- [ ] 失败能取得日志、截图和 Trace。
- [ ] 提交前和 PR 中都有自动检查。
- [ ] 测试环境不连接生产数据库。
- [ ] 新 Bug 修复同时增加回归测试。

相关笔记：

- [[pytest]]
- [[Playwright]]
- [[API 产品化]]
- [[Web 用户认证与安全]]
- [[CI-CD|CI/CD]]
- [[Debugging 与可观测性]]
- [[系统集成 Runbook]]

## 八、测试矩阵与发布门禁

| 测试层 | 保护什么 | 典型触发 |
| --- | --- | --- |
| 单元 | 纯逻辑、解析、映射和权限函数 | 每次提交 |
| 集成 | 数据库、队列、外部 API 适配 | PR / nightly |
| 契约 | API、Webhook、Schema 兼容 | 接口变更 |
| E2E | 关键用户旅程 | 发布前 |
| 负载 | 并发、队列、限流和 p95 | 里程碑 |
| 安全 | 越权、注入、敏感日志和依赖 | PR / 定期 |
| AI 回归 | Prompt、模型、检索和工具变化 | AI 发布 |

Flaky Test 不应靠无限重试隐藏。每次重试都要记录失败类型、环境、Trace 和是否可复现，并在修复或隔离后恢复门禁。
