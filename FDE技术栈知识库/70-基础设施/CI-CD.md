---
title: CI/CD
aliases: [CI, CD, 持续集成, 持续部署, 流水线, Pipeline]
tags: [fde, infra, devops, automation]
created: 2026-08-24
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
- [[Debugging 与可观测性]] —— 上线后要看
