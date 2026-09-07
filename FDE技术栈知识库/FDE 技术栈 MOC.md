---
title: FDE 技术栈 MOC
aliases: [FDE 技术栈地图, FDE Tech Stack Map, FDE 知识库索引]
tags: [fde, moc, index]
created: 2026-08-24
---

# FDE 技术栈 MOC

> [!abstract] 这是什么
> 这是 **FDE（Forward Deployed Engineer，前线部署工程师）** 技术栈知识库的 **地图（Map of Content）**。
> 所有细分板块的原子笔记都从这里出发，用 `[[wikilinks]]` 相互连接。
> 阅读顺序建议：先建立 [[FDE 角色定义]] 的心智模型，再看 [[FDE 工作方式]] 与 [[FDE 能力模型]]，然后按 [[FDE 学习路线]] 逐层深入。

---

## 🧭 一、先理解「人」——FDE 是什么

- [[FDE 角色定义]] —— FDE 与传统研发的本质区别
- [[FDE 工作方式]] —— 模糊需求下的快速交付循环
- [[FDE 能力模型]] —— 技术 / 业务 / 交付三位一体
- [[FDE 学习路线]] —— 项目驱动的五阶段学习顺序
- [[FDE 练习项目]] —— 三个值得做透的端到端项目

---

## 💻 二、编程语言（地基）

- [[Python]] —— AI FDE 第一优先级语言
- [[TypeScript]] —— Web 应用 / 前端 Demo / Node 服务

### Python 生态子工具（点 [[Python]] 展开）

- [[FastAPI]] —— Web API 框架
- [[HTTP 客户端]] —— requests / httpx，HTTP 请求
- [[pandas]] —— DataFrame 数据处理
- [[asyncio]] —— 异步并发
- [[subprocess]] —— 调用系统命令
- [[Pydantic]] —— 数据校验 / 配置
- [[SQLAlchemy]] —— ORM / 数据库
- [[pytest]] —— 测试

---

## 🎨 三、前端（让客户「看见能跑」）

- [[React]] —— 组件化 UI 基础
- [[Next.js]] —— 全栈 React 框架，FDE Demo 利器
- [[Tailwind CSS]] —— 原子化 CSS，快速出界面

---

## ⚙️ 四、后端（把东西连起来）

> [!note] Python 的 Web 框架在哪？
> [[FastAPI]] 已归入上方「Python 生态子工具」，因为它是 Python 的具体框架，随 Python 一起学更顺。后端这里保留跨语言的接口与运行时基础。

- [[后端基础]] —— 后端是什么、请求生命周期、本地运行也要 HTTP
- [[Node.js]] —— JS 运行时，轻量服务与 SDK
- [[REST API]] —— REST 与 GraphQL 的接口设计基础
- [[微服务]] —— 为什么有几十个服务 / 容器，以及编排需求

---

## 🗄️ 五、数据（存储与流转）

- [[PostgreSQL]] —— 主力关系型数据库
- [[SQL]] —— 查询语言与数据操作基本功
- [[Redis]] —— 缓存 / 会话 / 队列 / 限流
- [[ETL 与数据管道]] —— 数据抽取、转换、加载与管线

---

## 🤖 六、AI（FDE 的核心战场）

- [[LLM API]] —— 模型调用的底层认知（Token / 流式 / 成本）
- [[Prompt 工程]] —— 把模糊需求翻译成模型指令
- [[Structured Output]] —— 让模型产出可程序消费的结构化数据
- [[Tool Calling]] —— 模型调用外部工具的能力
- [[RAG]] —— 检索增强生成全流程
- [[Embedding]] —— 向量化与相似度检索
- [[Agent]] —— 自主规划与执行的智能体
- [[MCP]] —— 模型上下文协议，工具标准化

### Agent 进阶：设计原理与工程实践

> [!tip] 一条从「能跑」到「可靠」的主线
> 核心公式 **Agent = LLM + 上下文 + 工具**——上下文是眼睛、LLM 是大脑、工具是手脚。
> 阅读顺序建议：[[Harness 工程]]（总框架）→ [[上下文工程]] / [[KV Cache]] / [[上下文压缩]]（眼睛）→ [[工具设计原则]] / [[Agent Skills]]（手脚）→ [[记忆系统]] / [[Agentic RAG]]（跨会话知识）→ [[Coding Agent]]（元能力）→ [[Agent 评估]]（怎么变好）→ [[模型后训练]] / [[Agent 持续进化]]（能力提升）→ [[多 Agent 协作]]（群体系统）。

**基础架构层**

- [[Harness 工程]] —— Agent = Model + Harness；约束/验证/纠正五要素与编排模式
- [[上下文工程]] —— 上下文是「眼睛」：静态前缀 + 轨迹、提示工程、状态栏
- [[KV Cache]] —— 前缀稳定性 = 更快更便宜；三条铁律与错误模式
- [[上下文压缩]] —— 三个动机、六种策略对比、生产五层机制、隔离优于压缩
- [[Agent Skills]] —— 领域能力的可组合单元与渐进式披露
- [[工具设计原则]] —— ACI、粒度权衡、Sidecar 安全审查、主动工具发现
- [[提示注入]] —— 上下文安全的核心威胁与三层防御

**知识与记忆层**

- [[记忆系统]] —— 用户记忆：层次结构、四种存储格式、双层记忆架构
- [[Agentic RAG]] —— 混合检索、结构化索引、上下文感知检索与智能体化检索

**能力构建层**

- [[Coding Agent]] —— 代码是通用 Agent 的元能力；Harness 实践与故障恢复
- [[Agent 评估]] —— Pass@k vs Pass^k、LLM-as-a-Judge、Rubric 与可观测性（跨链 [[Debugging 与可观测性]]）
- [[模型后训练]] —— 预训练→Mid-training→SFT→RL 全景；SFT 记忆、RL 泛化
- [[Agent 持续进化]] —— 经验→知识/指令/程序/参数四种更新载体
- [[多 Agent 协作]] —— 共享/隔离上下文 × 对等/管理者/去中心化；失败模式

---

## 🧠 六点五、DeepSeek Harness（Agent 框架深度剖析）

> [!tip] 从零到一完全指南
> 一套 **21 篇递进式笔记**，让零基础读者从第一性原理理解 DeepSeek Harness 的架构，并具备开发能力。
> 源码仓库：[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)

### 学习路线

- [[00-学习路线图]] —— 总览 + 导航 + 预计时间
- [[01-前置知识]] —— 最小必要基础（函数、变量、JSON、终端）
- [[02-核心概念]] —— Agent = LLM + 工具 + 循环（类比讲解）
- [[03-理解你每天在用的东西]] —— 从用户体验倒推内部机制

### 技术基础

- [[04-TypeScript 速成]] —— 最小 TS 知识（读懂 Harness 代码）
- [[05-Node.js 与 npm 速成]] —— 运行环境理解
- [[06-Cordis 插件系统]] —— Harness 的骨架（微内核）

### 核心机制

- [[07-Agent Loop 深度拆解]] —— ReAct 循环的源码级讲解
- [[08-工具系统]] —— 工具注册、调度、执行
- [[09-Session 日志]] —— Append-Only 事件流
- [[10-记忆与上下文]] —— 短期/长期记忆工程实现

### 高级能力

- [[11-子 Agent 与多 Agent]] —— 委派与协作
- [[12-Preset 与配置]] —— 如何组合一个 Agent
- [[13-Skill 与 Goal 系统]] —— 高级功能
- [[14-Sandbox 与安全]] —— 沙箱、审批、权限

### 动手实践

- [[15-从零写一个最小 Agent]] —— Python 版，逐行注释
- [[16-对比与总结]] —— Agent.md vs Harness 完整映射表

### 深度专题

- [[17-ReAct 深度解析与 Agent 架构层级详解]] —— ReAct 原理 + 架构层级 + Session Log + 插件化 + 多 Agent + 安全 + 流式 Token + Goal

### 附录

- [[附录A-术语表]] —— 全部术语中英对照
- [[附录B-源码地图]] —— 54 个包的功能索引
- [[附录C-常见问题]] —— FAQ

---

## 🤖 七、自动化（替代重复劳动）

- [[Playwright]] —— 浏览器自动化与数据抓取
- [[Webhook]] —— 事件驱动的实时回调
- [[Cron]] —— 定时任务与周期作业
- [[事件驱动 Agent]] —— 异步与事件驱动架构：事件触发、打断恢复、语音交互
- [[Computer Use]] —— GUI 自动化 Agent：视觉定位、观察接口与机器人延伸

---

## 🐧 八、基础设施（能写出来也要能部署）

- [[Linux]] —— 命令行与服务器排查
- [[Docker]] —— 容器化交付
- [[Docker Compose]] —— 多服务编排
- [[云平台]] —— AWS / GCP / Azure 选一个深入
- [[国内云]] —— 阿里云 / 腾讯云 / 火山引擎 / 华为云
- [[云服务模型]] —— IaaS / PaaS / SaaS / FaaS 责任档位
- [[部署方式]] —— 六种部署形态全景（裸金属→静态边缘）
- [[Serverless]] —— FaaS 函数即服务与场景
- [[静态托管与边缘]] —— CDN / 边缘函数 / Agent 部署原理
- [[DevOps]] —— 交付文化与 CI/CD 测试本质
- [[CI/CD]] —— 持续集成与持续部署

---

## 🔌 九、系统集成（FDE 的核心价值）

- [[认证与授权机制]] —— API Key/OAuth/JWT/Webhook/Token 生命周期总览 + 授权框架哲学 + 匿名化实战
- [[OAuth]] ——  delegated 授权框架
- [[JWT]] —— 无状态令牌鉴权
- [[SaaS 集成]] —— Salesforce / Slack / Notion 等
- [[企业系统集成]] —— CRM / ERP / 内部系统的连接

---

## 🛠️ 十、工程能力（普通 Demo 与优秀 FDE 的分水岭）

- [[Git]] —— 版本控制与协作
- [[Debugging 与可观测性]] —— 出问题后快速定位（含 Agent Trace 树与评估闭环）
- [[System Design]] —— 基本系统设计能力
- [[Agent 评估]] —— Agent 侧的系统化评估（环境 / 数据集 / LLM-as-a-Judge）

---

## 🏢 九点五、Palantir Ontology（企业数字孪生与操作语义层）

> [!tip] 为什么 FDE 要了解 Palantir Ontology
> Ontology 是 Palantir 的核心架构，也是 AI Agent 落地的关键模式。
> 理解 Ontology = 理解"如何让 AI Agent 可靠地操作企业业务"。

- [[Palantir Ontology 核心概念]] —— 什么是 Ontology，为什么它重要
- [[Palantir Ontology 三层架构]] —— 语义层、动力层、动态层的详细拆解
- [[Palantir Ontology 与传统方案对比]] —— 与 ETL、BI、知识图谱、数据中台的区别
- [[Palantir Ontology 落地案例]] —— 供应链、医院、食品追溯等真实场景
- [[Palantir FDE 与 Ontology]] —— FDE 模式为什么需要 Ontology，以及 FDE 的局限
- [[Palantir AIP 与 AI 集成]] —— LLM 如何通过 Ontology 操作业务（OAG、Scenario Branching、AI FDE）

---

## 🔗 跨板块主线

> [!tip] 如何用这个知识库
> - 每个笔记都是 **原子化** 的：一个技术 / 概念一篇，方便链接与复用。
> - 用 Obsidian 的 **图谱视图（Graph View）** 可以看到这些笔记如何连成网络。
> - 用 `[[笔记名]]` 双向链接跳转；用标签 `#fde` 聚合检索。
> - 遇到重叠主题（如 Webhook 同时出现在自动化与集成），以 **同一篇笔记 + 多处链接** 的方式避免信息分裂。

> [!info] 体系化材料的融入说明
> 《深入理解 AI Agent：设计原理与工程实践》（李博杰，306 页）的全部内容已**分散融入**本库各板块，未单开模块：
>
> | 书籍章节 | 融入位置 |
> | --- | --- |
> | 第 1 章 入门 / Harness 工程 | [[Harness 工程]]、[[Agent]] |
> | 第 2 章 上下文工程 | [[上下文工程]]、[[KV Cache]]、[[上下文压缩]]、[[Agent Skills]]、[[提示注入]] |
> | 第 3 章 记忆与知识库 | [[记忆系统]]、[[Agentic RAG]] |
> | 第 4 章 工具 | [[工具设计原则]]、[[MCP]]、[[Tool Calling]] |
> | 第 5 章 Coding Agent | [[Coding Agent]] |
> | 第 6 章 交互扩展 | [[事件驱动 Agent]]、[[Computer Use]]（60-自动化） |
> | 第 7 章 评估 | [[Agent 评估]]、[[Debugging 与可观测性]] |
> | 第 8 章 模型后训练 | [[模型后训练]] |
> | 第 9 章 持续进化 | [[Agent 持续进化]] |
> | 第 10 章 多 Agent 协作 | [[多 Agent 协作]] |
>
> 与 [[00-学习路线图|DeepSeek Harness 系列]] 的关系：Harness 系列讲**源码实现**，上述笔记讲**设计原理**，二者经 [[Harness 工程]] 互链互补。母本长文末尾的「第 23 章 AI Agent 进阶」是本部分的长文速览。
