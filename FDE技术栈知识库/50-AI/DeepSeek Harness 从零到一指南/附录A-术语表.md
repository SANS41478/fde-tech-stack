---
title: 术语表 — 中英对照
aliases:
  - Glossary
  - 术语
tags:
  - deepseek-harness
  - 术语
  - 附录
created: 2026-08-31
---

# 附录 A — 术语表

> [!tip] 使用方式
> 遇到不懂的术语，来这里查。按字母顺序排列。

---

## A

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Agent | Agent | 能自主执行任务的 AI 系统 = LLM + 工具 + 循环 |
| Agent Loop | Agent Loop | Agent 的核心循环：接收消息 → 调用 LLM → 执行工具 → 重复 |
| Append-Only | Append-Only | 只能追加、不能修改的日志设计 |
| async/await | async/await | 等待异步操作完成的语法 |

## B

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Bundle | Bundle | Cordis 插件包的分发格式 |

## C

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Capability Seam | Capability Seam | 标准化的接口，实现可替换 |
| CLI | Command Line Interface | 命令行界面 |
| Compaction | Compaction | 上下文压缩，防止对话过长 |
| Context | Context | 存放所有插件服务的仓库 |
| Cordis | Cordis | Harness 的底层微内核插件框架 |

## D

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Delegation Depth | Delegation Depth | 子 Agent 的嵌套层数限制 |
| deriveMessages | derive Messages | 从 Session Log 推导 LLM 需要的消息历史 |

## E

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| ESM | ES Module | JavaScript 模块导入导出格式 |
| Event | Event | 插件间的通信机制 |
| Exclusive | Exclusive | 工具串行执行模式 |

## G

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Goal | Goal | 有状态的任务追踪系统 |

## I

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Inbox | Inbox | Agent 的消息队列（next-turn / next-step）|
| Interface | Interface | 定义数据结构的合同 |

## J

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| JSON | JSON | 结构化数据格式 |
| JSONL | JSONL | 每行一个 JSON 的日志格式 |

## L

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| LLM | Large Language Model | 大语言模型（如 DeepSeek Chat）|

## M

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| MCP | Model Context Protocol | 模型上下文协议 |
| monorepo | monorepo | 一个项目包含多个子项目 |

## N

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Node.js | Node.js | 在电脑上运行 JavaScript 的环境 |
| npm | Node Package Manager | 包管理器 |
| pnpm | Performant npm | 更快的包管理器 |

## P

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Parallel | Parallel | 工具并行执行模式 |
| Plugin | Plugin | 可插拔的功能模块 |
| Preset | Preset | Agent 的功能预设组合 |
| Profile | Profile | 完整的配置方案 |
| Provider | Provider | LLM 的服务提供商 |

## R

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| ReAct | Reasoning + Acting | 思考-行动循环模式 |
| ReactLoopAgent | ReactLoopAgent | Harness 的 Agent Loop 实现类 |
| Reversible Effects | Reversible Effects | 插件卸载时自动清理的效果 |

## S

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Sandbox | Sandbox | 隔离的执行环境 |
| Schema | Schema | 数据格式的描述（如 JSON Schema）|
| Session | Session | 一次完整的对话会话 |
| Session Log | Session Log | Agent 的完整事件日志 |
| Skill | Skill | 按需加载的知识文件 |
| Step | Step | 一次 LLM 调用 + 工具执行 |
| Surface | Surface | 有序消息面 |

## T

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Tool | Tool | Agent 可以使用的工具 |
| Tool Call | Tool Call | LLM 请求使用某个工具 |
| Tool Result | Tool Result | 工具执行的结果 |
| TypeScript | TypeScript | JavaScript + 类型系统 |
| Turn | Turn | 一个完整的工作轮次（可能包含多个 Step）|

## W

| 术语 | 英文 | 一句话解释 |
|---|---|---|
| Waterfall | Waterfall | 传递接力棒的事件模式 |

---

## 相关笔记

- [[01-前置知识]] — 编程基础术语
- [[06-Cordis 插件系统]] — Cordis 术语
- [[07-Agent Loop 深度拆解]] — Loop 术语
- [[09-Session 日志]] — 日志术语
