# FDE 技术栈知识库

> FDE（Forward Deployed Engineer，前线部署工程师）技术栈的 **Obsidian 风格知识库**。
> 一份主指南 + 一套原子化笔记，按「语言 / 前端 / 后端 / 数据 / AI / 自动化 / 基础设施 / 系统集成 / 工程能力」分层拆解。

## 这是什么

本项目把一份 FDE 技术栈完整指南，拆成可在 [Obsidian](https://obsidian.md) 中使用的**双向链接知识库**：

- **原子化笔记**：一个技术 / 概念一篇，便于链接与复用。
- **双向链接**：全文用 `[[wikilinks]]` 互相连接，图谱视图可见知识网络。
- **统一结构**：每篇按「定位 → 为什么 → 实战示例 → 常见坑 → 相关笔记」展开。
- **Callout 提示框**：用 Obsidian 原生 `> [!note] / [!tip] / [!warning]` 区分要点、经验与坑。

## 目录结构

```text
FDE技术栈知识库/
├── FDE 技术栈 MOC.md        # 总索引（Map of Content），从这里进入
├── 00-概念/                 # 角色定义 / 工作方式 / 能力模型 / 学习路线 / 练习项目
├── 10-编程语言/
│   ├── Python.md            # Python 语言本身
│   ├── TypeScript.md
│   └── Python 生态/         # Python 的「子节点」：FastAPI / pandas / asyncio / Pydantic / SQLAlchemy / pytest / subprocess / httpx
├── 20-前端/                 # React / Next.js / Tailwind CSS
├── 30-后端/                 # Node.js / REST API
├── 40-数据/                 # PostgreSQL / SQL / Redis / ETL 与数据管道
├── 50-AI/                   # LLM API / Prompt / Structured Output / Tool Calling / RAG / Embedding / Agent / MCP
├── 60-自动化/               # Playwright / Webhook / Cron
├── 70-基础设施/             # Linux / Docker / Docker Compose / 云平台 / CI-CD
├── 80-系统集成/             # OAuth / JWT / SaaS 集成 / 企业系统集成
└── 90-工程能力/             # Git / Debugging 与可观测性 / System Design
```

另有一份原始长文：`FDE（Forward Deployed Engineer）技术栈完整指南.md`，是整套笔记的母本。

## 怎么用

1. 用 **Obsidian** 打开 `FDE技术栈知识库/` 文件夹（或把整个仓库作为 vault）。
2. 从 `FDE 技术栈 MOC.md` 进入，顺着 `[[双链]]` 浏览。
3. 打开 **图谱视图（Graph View）** 查看各板块如何连成网络。
4. 用标签 `#fde` 聚合检索所有笔记。

## 职能地图（比「前后端」更全的视角）

技术栈不只是"前端 vs 后端"，按职能可分为 7 类：

| 职能层 | 负责什么 | 本库对应 |
|---|---|---|
| 应用层 | 前端（界面）/ 后端（API） | React / Next.js / FastAPI / Node.js |
| 数据层 | 存储 / 处理 / ETL | PostgreSQL / SQL / Redis / pandas |
| AI 层 | 模型编排（FDE 核心） | LLM API / RAG / Agent / MCP / Pydantic |
| 集成层 | 连外部系统 | httpx / OAuth / SaaS / 企业系统 |
| 自动化层 | 替代重复劳动 | subprocess / Playwright / Cron |
| 基础设施层 | 能部署能跑 | Linux / Docker / 云平台 / CI-CD |
| 工程能力层 | 质量与可维护 | pytest / Git / Debugging / System Design |

> Python 是 FDE 的主力语言，不是因为"写后端"，而是因为它横跨数据、AI、集成、自动化、工程能力多个职能层。

## 说明

- `.workbuddy/` 与 `.obsidian/` 为本地隐私 / 配置数据，已被 `.gitignore` 排除，不纳入版本库。
- 笔记中的 `[[链接]]` 按笔记名解析，移动文件不会断链。

---

*本仓库用于个人学习与 FDE 知识沉淀。*
