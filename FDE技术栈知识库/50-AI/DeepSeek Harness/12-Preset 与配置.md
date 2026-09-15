---
title: Preset 与配置 — 如何组合一个 Agent
aliases:
  - Agent Preset
  - 配置系统
tags:
  - deepseek-harness
  - preset
  - 配置
created: 2026-08-31
type: tutorial
domain: ai
layer: implementation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# Preset 与配置 — 如何组合一个 Agent

> [!tip] 目标
> 理解如何通过 Preset 系统配置不同类型的 Agent。

---

## 1. 什么是 Preset

> [!tip] 类比：套餐
> Preset = 快餐店的**套餐**：
>
> - **标准套餐**：汉堡 + 薯条 + 可乐（全功能）
> - **最小套餐**：汉堡 + 水（基本功能）
> - **豪华套餐**：汉堡 + 薯条 + 可乐 + 沙拉 + 甜点（超级全功能）
>
> 你选哪个套餐，就得到对应的功能组合。

在 Harness 里：

| Preset | 内容 | 用途 |
|---|---|---|
| `standard` | 全部工具 + 技能 + Goal + 子 Agent | 日常开发 |
| `minimal` | 只有 bash + 文本编辑器 | 测试模型 |
| `headless` | 无服务器的一次性运行 | 自动化任务 |

---

## 2. Preset 的组成

一个 Preset 由两部分组成：

### 2.1 preset.yml — 元数据

```yaml
# preset.yml
name: 标准模式
description: 完整的编程助手，包含所有工具和技能
order: 1  # UI 中的显示顺序
```

### 2.2 agent.cordis.yml — 插件组合

```yaml
# agent.cordis.yml
- id: persona
  name: "@deepseek-ai/dsh-persona"
  config:
    persona: "你是一个有帮助的编程助手"

- id: shell
  name: "@deepseek-ai/dsh-shell"
  config:
    persistent: true

- id: tools-fs
  name: "@deepseek-ai/dsh-tool-fs"

- id: tools-bash
  name: "@deepseek-ai/dsh-tool-bash"

- id: skills
  name: "@deepseek-ai/dsh-skill"

- id: goals
  name: "@deepseek-ai/dsh-goal"

- id: subagent
  name: "@deepseek-ai/dsh-subagent"
```

每一行就是一个**插件条目**：
- `id`：唯一标识
- `name`：插件包名
- `config`：插件配置（可选）
- `disabled`：是否禁用（可选，支持 JS 表达式）

---

## 3. 标准 Preset vs 最小 Preset

| 特性 | 标准 Preset | 最小 Preset |
|---|---|---|
| 人格 | ✅ | ✅ |
| Bash 工具 | ✅ | ✅ |
| 文件工具 | ✅ | ✅ |
| 文本编辑器 | ✅ | ✅ |
| Web 搜索 | ✅ | ❌ |
| 技能系统 | ✅ | ❌ |
| Goal 系统 | ✅ | ❌ |
| 子 Agent | ✅ | ❌ |
| 工作流 | ✅ | ❌ |
| 审批系统 | ✅ | ❌ |

**最小 Preset 的配置**（只有几行）：

```yaml
- id: persona
  name: "@deepseek-ai/dsh-persona"
  config:
    persona: "你是一个有帮助的编程助手"

- id: shell
  name: "@deepseek-ai/dsh-shell"
  config:
    persistent: true

- id: tools-editor
  name: "@deepseek-ai/dsh-tool-editor"
```

---

## 4. Profile — 预设的叠加

> [!tip] 类比：装修方案
> Profile = **完整的装修方案**：
>
> - 列出需要哪些 Bundle（哪些家具包）
> - 定义叠加顺序（先放什么，后放什么）
> - 保存用户自定义（用户改了什么）

Harness 内置了两个 Profile：

### web Profile

```
dsh-base（基础层）
  └─ 模型适配、工具、持久化、沙箱、审批...

dsh-web-app（Web 应用层）
  └─ Web UI、浏览器工具...
```

### headless Profile

```
dsh-base（基础层）

dsh-headless（无界面层）
  └─ 一次性运行器...
```

---

## 5. Patch Layer 系统 — 层叠配置

> [!tip] 类比：Photoshop 图层
> Patch Layer = **Photoshop 的图层**：
>
> - 底层：基础配置
> - 中层：Profile 配置
> - 顶层：用户自定义
>
> 顶层覆盖中层，中层覆盖底层。

**层级应用顺序**：

```
1. Bundle 层（按 profile 列出的顺序）
   ↓
2. Profile 的 cordis.patch.yml
   ↓
3. Home 级的 cordis.patch.yml
   ↓
4. --patch 命令行参数
```

**用户自定义示例**：

```yaml
# ~/.dsh/cordis.patch.yml
# 覆盖默认的 LLM 配置
- id: llm
  config:
    provider: deepseek
    model: deepseek-coder
```

---

## 6. 查看当前配置

```bash
# 打印完整的插件树
dsh --profile web --dump-config

# 输出示例：
# entries:
#   - id: llm-deepseek
#     name: "@deepseek-ai/dsh-llm-deepseek"
#     config:
#       provider: deepseek
#       model: deepseek-chat
#   - id: tools
#     name: "@deepseek-ai/dsh-tools"
#   - id: session
#     name: "@deepseek-ai/dsh-session"
#   ...
```

---

## 7. 运行时切换 Preset

用户可以通过 `/preset` 命令在运行时切换 Preset：

```
/preset minimal    ← 切换到最小模式
/preset standard   ← 切换到标准模式
```

> [!note] 源码位置
> `packages/preset/agent-presets/` — Preset 管理

---

## 小结

| 概念 | 一句话解释 | 类比 |
|---|---|---|
| Preset | Agent 的功能套餐 | 快餐套餐 |
| Profile | 完整的配置方案 | 装修方案 |
| Bundle | 功能包的标准包装 | 家具包 |
| Patch Layer | 层叠配置覆盖 | Photoshop 图层 |
| cordis.yml | 插件组合配置 | 家具清单 |

---

## 下一步

理解了配置系统后，我们来看看 Harness 的高级功能：[[13-Skill 与 Goal 系统]]。
