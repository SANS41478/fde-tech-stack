---
title: DevOps
aliases: [DevOps 工程师, 研发运维, 持续交付文化]
tags: [fde, infra, devops, cicd]
created: 2026-08-27
type: reference
domain: infra
layer: foundation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# DevOps

> [!abstract] 定位
> **DevOps** = Development + Operations，是打破「开发写代码 / 运维部署维护」之墙的方法论；落地的「DevOps 工程师」负责搭自动化流水线、管基础设施、做监控告警、保障可靠性。它与 [[CI-CD|CI/CD]] 强绑定：CI/CD 是把 DevOps 理念变成可执行自动化的发动机。

---

## 一、为什么和 CI/CD 强绑定

DevOps 说「要频繁、自动、可靠地交付」，但这是句空话；[[CI-CD|CI/CD]] 把它变成可运行的流水线（每次变更自动构建 + 测试 + 部署）。没有 CI/CD，DevOps 无抓手。

---

## 二、测试与自动化的边界

DevOps 关注的是让团队持续、可靠地交付；具体的测试类型、流水线步骤和 GitHub Actions 配置统一收录在 [[CI-CD|CI/CD]]。

AI 可以辅助生成测试、流水线配置和失败分析，但期望行为、质量门槛和发布权限仍需由人定义。

---

## 三、AI 能全自动 CI/CD，未来就没 CI/CD 了？

不会消失，只会变成「AI 辅助」：

- CI/CD 的存在意义是「每次变更都自动构建 + 测试 + 部署」这个**机制**，跟谁写测试无关——机制永远需要。
- AI 替掉的是「写测试 / 配流水线」的人力，但流程框架照常运行。
- 所以未来是 AI 减少手工编写，CI/CD 流程本身继续存在。

---

## 四、FDE 视角

- FDE 不必是 DevOps 专家，但要懂基础：能用 [[Git]] + [[CI-CD|CI/CD]] 让自己的方案可重复上线，而不是手动 scp。
- 掌握基础后，敢改、快交付、可回滚，契合 [[FDE 工作方式]] 的快速迭代。

---

相关笔记：
- [[CI-CD|CI/CD]] —— 流水线具体怎么跑
- [[Git]] —— 触发源与版本管理
- [[部署方式]] —— 部署形态全貌
- [[Docker]] —— 流水线构建产物
- [[云平台]] —— 部署目标
- [[pytest]] —— 测试怎么写
- [[System Design]] —— 可靠性设计
