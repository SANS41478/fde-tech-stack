---
title: FDE 学习路线
aliases: [FDE 学习顺序, FDE 怎么学, FDE roadmap]
tags: [fde, concept, learning]
created: 2026-08-24
type: concept
domain: concept
layer: foundation
canonical: false
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: evergreen
sources: [本库综合整理；以相关技术主题的官方文档与交付实践为依据]
---

# FDE 学习路线

> [!abstract] 核心
> FDE 不适合传统程序员的「先学完基础再动手」路线（Python → C++ → 数据结构 → OS → 编译原理…）。FDE 更适合 **项目驱动**：先有能跑的东西，再在缺口处补知识。下面是一套五阶段顺序。

---

## 一、为什么不走传统路线

传统路线假设「基础打牢才能干活」。但 FDE 的护城河是 **把技术快速拼成可用方案**，而不是成为某个领域的理论专家。过早陷入底层原理，会拖慢「能交付」的节奏。

> [!tip] 项目驱动原则
> 每学一个技术，立刻用它解决一个具体问题；遇到不会的，再针对性补。

---

## 二、五阶段顺序

### 第一阶段：能写能连
```text
Python
  ↓
HTTP / API
  ↓
FastAPI
  ↓
PostgreSQL
```
目标：能写脚本、能调 API、能起一个后端服务、能存数据。
- 起点：[[Python]]
- 接口基础：[[REST API]]
- 后端框架：[[FastAPI]]
- 存储：[[PostgreSQL]]、[[SQL]]
- 产品入口：先用 [[产品验证与用户访谈]] 确认问题和用户

### 第二阶段：能让人看见
```text
React
  ↓
Next.js
  ↓
TypeScript
```
目标：能做出客户可点击的界面，验证价值。
- [[React]] → [[Next.js]] → [[TypeScript]]
- 样式加速：[[Tailwind CSS]]
- 体验与设计：[[UI UX、设计系统与动效]]
- 需求落地：[[PRD 与技术文档]]

### 第三阶段：能部署
```text
Linux
  ↓
Docker
  ↓
Docker Compose
  ↓
Cloud
```
目标：把前面搭的东西真正跑在服务器上。
- [[Linux]] → [[Docker]] → [[Docker Compose]] → [[云平台]]
- 本地运行：[[Node.js 项目环境与本地运行]]
- 公网接入：[[公网访问、域名与 HTTPS]]
- 服务器路线：[[VPS 运维与 1Panel]]

### 第四阶段：能智能化
```text
LLM API
  ↓
Structured Output
  ↓
Tool Calling
  ↓
RAG
  ↓
Agent
  ↓
MCP
```
目标：把 AI 能力系统化地嵌进方案。
- 模型调用：[[LLM API]]
- 可控输出：[[Structured Output]]
- 工具使用：[[Tool Calling]]
- 知识检索：[[RAG]]、[[Embedding]]
- 自主执行：[[Agent]]、[[MCP]]

### 第五阶段：能集成
```text
Playwright
  ↓
Webhook
  ↓
SaaS Integration
  ↓
企业系统集成
```
目标：把方案焊进客户真实系统。
- 自动化：[[Playwright]]、[[Webhook]]、[[Cron]]
- 集成：[[SaaS 集成]]、[[企业系统集成]]、[[OAuth]]、[[JWT]]
- Web 产品化：[[API 产品化]]、[[Web 用户认证与安全]]

---

## 三、终点：真实客户问题

```text
真实客户问题
  ↓
快速 Prototype
  ↓
系统集成
  ↓
部署
  ↓
监控
  ↓
交付
```
这一步没有「学完」的那天——它就是工作本身。配套能力见 [[Debugging 与可观测性]] 与 [[System Design]]。

上线后的闭环：

```text
真实用户
  ↓
[[Web 测试与 E2E]] + [[SEO、分享与产品分析]]
  ↓
[[用户反馈与产品迭代]]
  ↓
下一轮 Prototype
```

---

## 四、给自学者的一句话

> [!quote]
> 不要等「准备好」再开始。FDE 的「准备好」，是 **第一个跑起来的 Demo** 定义的，不是课程定义的。

相关延伸：
- [[FDE 能力模型]] —— 学这些是为了获得什么能力
- [[FDE 练习项目]] —— 用项目巩固路线
- [[FDE 技术栈 MOC]] —— 各板块入口
