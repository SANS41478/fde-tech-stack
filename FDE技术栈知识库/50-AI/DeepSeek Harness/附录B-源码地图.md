---
title: 源码地图 — 54 个包的功能索引
aliases:
  - 源码索引
  - 包功能
tags:
  - deepseek-harness
  - 源码
  - 附录
created: 2026-08-31
type: reference
domain: ai
layer: implementation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# 附录 B — 源码地图

> [!tip] 使用方式
> 需要找某个功能的源码？来这里查。按分组排列。

---

## Core — 产品脊柱

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `core/session` | 会话日志 | Append-Only 事件流，单一事实来源 |
| `core/system-prompt` | 系统提示 | Prompt 组装和渲染 |
| `core/tools` | 工具注册表 | 工具注册、调度、执行 |
| `core/agent` | Agent 接口 | Agent 的类型定义和事件 |
| `core/agent-loop` | Agent Loop | ReAct 循环的默认实现 |
| `core/scope` | 作用域 | 每个 Agent 的注册边界 |
| `core/agent-default-model` | 默认模型 | Agent 的默认 LLM 配置 |
| `core/agent-tool-presentation` | 工具展示 | 工具结果的 UI 渲染 |

## LLM — 模型适配

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `llm/llm` | LLM 核心 | 消息词汇 + 适配器接口 |
| `llm/llm-deepseek` | DeepSeek 适配 | DeepSeek API 的具体实现 |
| `llm/llm-pi-ai` | PPIO 适配 | PPIO API 的具体实现 |
| `llm/llm-retry` | 重试策略 | LLM 调用失败时的重试 |
| `llm/token-meter` | Token 计量 | Token 用量统计 |

## Shell — 命令执行

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `shell/shell` | Shell 核心 | Bash 能力的 Service Definition |
| `shell/shell-local` | 本地 Shell | 本地 Bash 执行 |
| `shell/shell-pwsh` | PowerShell | PowerShell 执行 |

## Subagent — 多 Agent

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `subagent/subagent` | 子 Agent 核心 | 子 Agent 的 Service Definition |
| `subagent/subagent-fork-in-process` | Fork | 克隆当前会话 |
| `subagent/subagent-spawn-in-process` | Spawn | 创建全新 Agent |
| `subagent/subagent-acp` | ACP 委托 | 委托给外部系统 |
| `subagent/subagent-claude-code` | Claude 适配 | 委托给 Claude Code |
| `subagent/subagent-codex` | Codex 适配 | 委托给 Codex |
| `subagent/tool-subagent` | 子 Agent 工具 | 面向模型的子 Agent 工具 |
| `subagent/tool-subagent-control` | 子 Agent 控制 | 子 Agent 控制 |
| `subagent/tool-subagent-report` | 子 Agent 报告 | 子 Agent 结果报告 |

## Sandbox — 安全沙箱

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `sandbox/sandbox` | 沙箱核心 | 沙箱的 Service Definition |
| `sandbox/sandbox-local` | 本地沙箱 | 本地执行的沙箱 |
| `sandbox/sandbox-policy` | 沙箱策略 | 沙箱的访问策略 |
| `sandbox/sandbox-windows-acl` | Windows 权限 | Windows ACL 控制 |

## Session — 会话管理

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `session/session` | 会话核心 | 会话的持久化和投影 |
| `session/session-query` | 会话查询 | 会话数据的查询 |

## Interaction — 用户交互

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `interaction/user-approval` | 审批系统 | 危险操作的人类确认 |
| `interaction/commands` | 命令系统 | 斜杠命令 |
| `interaction/user-questions` | 问答系统 | Agent 向人类提问 |
| `interaction/permission-presets` | 权限预设 | 简化的安全级别 |

## Skill — 技能系统

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `skill/skill` | Skill 核心 | 技能注册表 |
| `skill/skill-filesystem` | 文件 Skill | 从文件系统发现 Skill |

## Goal — 目标系统

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `goal/goal` | Goal 核心 | 目标追踪服务 |
| `goal/tool-goal` | Goal 工具 | 面向模型的 Goal 工具 |
| `goal/goal-round-driver` | 自动继续 | Goal 完成一步后自动触发下一步 |

## 其他

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `mcp/mcp` | MCP 协议 | 模型上下文协议桥接 |
| `compaction/compaction` | 上下文压缩 | 防止对话过长 |
| `workflow/workflow` | 工作流 | 多步骤自动化 |
| `plan/plan` | Plan 模式 | 有状态的规划 |
| `fs/fs` | 文件系统 | 文件访问能力 |
| `web/web` | Web 能力 | 网页搜索和抓取 |
| `todo/todo` | 待办事项 | Todo 写入工具 |
| `guard/guard` | 守卫 | 循环卫生 + 工具超时 |
| `context/context` | 上下文 | 请求上下文插件 |
| `credentials/credentials` | 凭据 | API Key 管理 |
| `settings/settings` | 设置 | 用户设置 |
| `identity/identity` | 身份 | 匿名身份 |
| `feedback/feedback` | 反馈 | 用户反馈 |
| `spill/spill` | 溢出 | 大数据溢出处理 |
| `typert/typert` | 类型图 | 类型生成器 |
| `api/api` | API | 远程 BFF + RPC |
| `acp/acp` | ACP | 自动化 Agent Client Protocol |
| `sdk/sdk` | SDK | JSON-RPC 协议 + 客户端 |
| `boot/boot` | 启动 | 启动逻辑 |
| `bundle/bundle` | Bundle | 分发格式 |
| `preset/preset` | Preset | Agent 预设 |
| `host/host` | 主机 | 主机能力 |
| `hooks/hooks` | Hooks | Claude Code/Codex 钩子 |
| `jobs/jobs` | 后台任务 | 后台工作管理 |
| `lsp/lsp` | LSP | 语言服务器协议 |
| `util/util` | 工具 | 零依赖工具库 |
| `runtime-diagnostics/runtime-diagnostics` | 运行时诊断 | 运行时诊断 |
| `self-modification/self-modification` | 自修改 | Agent 自检/挂载插件 |
| `terminal/terminal` | 终端 | 持久化终端 |
| `subprocess/subprocess` | 子进程 | 进程管理 |
| `test-support/test-support` | 测试支持 | 测试基础设施 |
| `examples/examples` | 示例 | 演示用的 bundle |
| `e2b/e2b` | E2B | 远程沙箱 POC |

## Apps — 应用入口

| 包 | 功能 | 一句话解释 |
|---|---|---|
| `apps/cli` | CLI | dsh 命令行入口 |
| `apps/web` | Web | Web UI |
| `apps/desktop` | Desktop | 桌面应用 |

---

## 相关笔记

- [[06-Cordis 插件系统]] — 理解包的组织方式
- [[07-Agent Loop 深度拆解]] — 核心包的详细讲解
- [[08-工具系统]] — 工具包的详细讲解
- [[09-Session 日志]] — 日志包的详细讲解
