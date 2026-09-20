---
title: CI/CD
aliases: [CI, CD, 持续集成, 持续部署, 流水线, Pipeline]
tags: [fde, infra, devops, automation]
created: 2026-08-24
type: reference
domain: infra
layer: foundation
canonical: true
canonical_group: infra-cicd
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://opentelemetry.io/docs/]
---

# CI/CD（持续集成与持续部署）

> [!abstract] 定位
> **CI/CD** 是把「代码变更 → 自动测试 → 自动部署」串成流水线的实践。FDE 虽不必是 DevOps 专家，但掌握基础 CI/CD 能让自己交付的方案 **稳定、可重复地上线**，而不是每次手动 scp。

---

## 一、CI vs CD

- **CI（Continuous Integration，持续集成）**：每次 push 自动跑构建 + 测试，尽早发现错误。
- **CD（Continuous Deployment，持续部署）**：通过测试后自动部署到环境（或一键批准部署）。

```text
Git Push
   ↓ CI：lint / test / build
   ↓ 通过？
CD：构建 [[Docker]] 镜像 → 推云 → 部署
```

---

## 二、FDE 常用工具

```text
GitHub Actions     # 与 [[Git]] 同源，最易上手
GitLab CI          # GitLab 内置
CircleCI / Jenkins # 通用
云原生：AWS CodePipeline / GCP Cloud Build
```

> [!note] 与 [[Git]] 的关系
> CI/CD 由 Git 事件（push / PR / tag）触发，是工程协作的延伸。

> [!note] 与 [[DevOps]] 的关系
> DevOps 是「频繁自动可靠交付」的方法论，CI/CD 是它的发动机。详见 [[DevOps]] 对角色、测试本质、AI 辅助的讨论。

---

## 三、一个最小 GitHub Actions 示例

```yaml
name: deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t myapp .
      - run: docker run myapp pytest   # 测试
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "推镜像 + 部署到 [[云平台]]"
```
> 真实部署步骤接云 Registry 与服务器，密钥用仓库 Secrets。

### Git Hooks 与分支环境

将快速检查放在本地 Hook，将完整验证放在 CI：

```text
提交前：format / typecheck / lint / unit test
Pull Request：build / API test / 关键 E2E / 安全扫描
合并 main：部署 preview 或 production
```

推荐让 `main` 始终可部署，功能在分支完成；高风险改动使用 Preview、Feature Flag 或小流量灰度，详见 [[Git]]、[[Web 测试与 E2E]]、[[用户反馈与产品迭代]]。

---

## 三·补、流水线到底「测」什么

常见误解：以为 CI 是 AI 现分析源码做测试。实际是**工程师事先写好测试用例，流水线只负责自动执行**：

- **单元测试**：测单个函数 / 类（pytest、JUnit，见 [[pytest]]）。
- **集成测试**：测多模块协作（如「下单」是否真写了库）。
- **端到端测试（E2E）**：模拟用户点页面操作。
- **静态检查 / Lint / 类型检查**：代码风格、类型错误。
- **安全 / 依赖漏洞扫描**：密钥泄露、已知 CVE。

> [!tip] AI 能否取代 CI/CD？
> 不会消失，只会变「AI 辅助」：AI 能帮写测试、写流水线 yaml、定位失败，但「每次变更自动构建+测试+部署」的机制永远需要，且 AI 生成的测试仍需人把关。流程框架照常运行。

---

## 四、FDE 为什么值得做

- **可重复**：手动部署易错，流水线每次一致。
- **敢改**：有测试 + 自动部署，改东西不怕。
- **快交付**：契合 [[FDE 工作方式]] 的快速迭代。
- **可回滚**：出问题一键回上一版。

---

## 五、常见坑

> [!warning]
> - **流水线无测试**：只 build 不 test，等于把 bug 自动上线。
> - **密钥泄露**：用 Secrets 而非明文；别 `echo $SECRET` 进日志。
> - **部署无健康检查**：上线即「以为成功」，实际服务没起来，加健康检查。
> - **直接部署生产无审批**：关键系统加人工批准一步。

---

相关笔记：
- [[Git]] —— 触发源与版本管理
- [[Docker]] —— 流水线构建的产物
- [[云平台]] —— 部署目标
- [[DevOps]] —— 交付文化与测试本质
- [[pytest]] —— 测试怎么写
- [[部署方式]] —— 部署形态全貌
- [[Debugging 与可观测性]] —— 上线后要看
- [[生产就绪与上线 Runbook]] —— 发布、灰度、回滚和事故处理

## 六、流水线的发布门禁

建议把流水线分成四类门禁：

1. **构建门禁**：依赖锁定、编译、Lint、类型检查和镜像扫描。
2. **行为门禁**：单元、集成、契约、E2E 和 AI 回归。
3. **安全门禁**：密钥扫描、依赖漏洞、权限和迁移审查。
4. **运营门禁**：健康检查、灰度、指标、告警和回滚脚本。

AI 生成的代码、测试和流水线配置与人工代码使用同样门禁，不能因为“只是 Demo”而跳过密钥与数据安全检查。
