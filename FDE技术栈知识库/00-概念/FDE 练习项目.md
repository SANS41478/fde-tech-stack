---
title: FDE 练习项目
aliases: [FDE 项目, FDE 练手项目, FDE portfolio]
tags: [fde, concept, project]
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

# FDE 练习项目

> [!abstract] 核心
> 相比刷算法题，FDE 更应该做 **完整的小项目**——每个项目都逼你把多个板块串起来，训练「从模糊想法到可运行系统」的能力。下面三个项目覆盖了 FDE 最常见的三类场景。

---

## 项目一：企业知识库（RAG 全流程）

```text
PDF
  ↓
Parser
  ↓
Embedding
  ↓
Vector DB
  ↓
RAG
  ↓
LLM
  ↓
Web UI
```

**技术组合**
- [[Python]] + [[FastAPI]] 后端
- [[PostgreSQL]] + pgvector（或 [[Embedding]] 专用向量库）
- [[LLM API]] 做生成
- [[Next.js]] 做问答界面
- [[Docker]] 打包部署

**训练点**
- 文档解析与分块（Chunking）
- 向量检索与重排（见 [[RAG]]、[[Embedding]]）
- 前后端联调与部署

> [!tip] 升级挑战
> 加 [[MCP]] 让知识库能被 Agent 调用；加权限控制让不同部门看到不同内容。

---

## 项目二：AI CRM 助手（系统集成）

```text
CRM
  ↓
API
  ↓
Data Processing
  ↓
LLM
  ↓
Customer Analysis
  ↓
Slack
```

**技术组合**
- [[REST API]] 拉取 CRM 数据
- [[OAuth]] 授权
- [[Python]] 做数据处理
- [[LLM API]] 做客户分析
- [[Webhook]] 把结果推到 Slack

**训练点**
- 真实 API 集成（鉴权、限流、分页）
- 数据清洗与结构化（[[Structured Output]]）
- 事件驱动通知

---

## 项目三：浏览器自动化 Agent（Agent + 抓取）

```text
User
  ↓
Agent
  ↓
Playwright
  ↓
Browser
  ↓
网站
  ↓
提取数据
  ↓
LLM
  ↓
结果
```

**技术组合**
- [[Agent]] 做规划与决策
- [[Tool Calling]] 让模型调用浏览器工具
- [[Playwright]] 实际控制浏览器
- [[Python]] 做异常兜底

**训练点**
- Agent 循环（规划 → 调用 → 观察 → 再规划）
- 浏览器自动化的稳定性（等待、重试、反爬）
- 异常处理——这是 Demo 与产品的分水岭

> [!warning] 常见坑
> 浏览器自动化最难的不是「能跑一次」，而是「能稳定跑一千次」。务必加超时、重试与日志（见 [[Debugging 与可观测性]]）。

---

## 如何把项目变成「作品集」

1. 先用 [[产品验证与用户访谈]] 记录目标用户、真实场景和 MVP 假设。
2. 用 [[PRD 与技术文档]] 固化范围、数据模型、API 和验收标准。
3. 每个项目都用 [[Git]] 管理，写好 README。
4. 用 [[Docker Compose]] 让别人一条命令跑起来。
5. 部署到 [[云平台]] 或 [[VPS 运维与 1Panel]]，给客户/面试官一个可访问的链接。
6. 用 [[Web 测试与 E2E]] 保护关键路径，用 [[SEO、分享与产品分析]] 观察真实使用。
7. 在笔记里记录「卡在哪里、怎么解决」——这比代码本身更值钱。

## 项目验收与失败演练

三个项目都必须补齐以下最小闭环：

| 维度 | 要求 |
| --- | --- |
| 数据 | 提供脱敏样例、边界样例和数据字典 |
| 质量 | 定义任务成功率、格式正确率或人工接受率 |
| 安全 | 至少覆盖权限不足、密钥泄露和越权访问 |
| 可靠性 | 模拟超时、429、重复事件、服务重启和部分失败 |
| 交付 | Docker Compose、一键启动、测试、监控和回滚说明 |
| 作品集 | 架构图、演示脚本、失败复盘和下一步路线 |

> [!tip] 作品集不是“功能截图”
> 最有说服力的材料是：原始问题、取样证据、关键取舍、失败样例、验收结果和上线后的指标变化。

相关延伸：
- [[FDE 学习路线]] —— 项目该按什么顺序做
- [[FDE 工作方式]] —— 项目背后的交付循环
- [[用户反馈与产品迭代]] —— 上线后的验证和成长
- [[FDE 技术栈 MOC]] —— 各技术入口
- [[FDE 交付 Playbook]] —— 项目从发现到交接
