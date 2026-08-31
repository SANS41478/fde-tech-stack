---
title: Skill 与 Goal 系统 — 高级能力
aliases:
  - 技能系统
  - 目标系统
tags:
  - deepseek-harness
  - skill
  - goal
created: 2026-08-31
---

# Skill 与 Goal 系统 — 高级能力

> [!tip] 目标
> 理解 Harness 的两个高级功能：Skill（技能）和 Goal（目标）。

---

## 1. Skill 系统 — 可加载的说明书

> [!tip] 类比：员工培训手册
> Skill = **按需加载的培训手册**：
>
> - 不是所有知识都塞进 System Prompt（那样太长了）
> - 而是把知识写成一个个 Skill 文件
> - Agent 需要时再加载对应的 Skill
>
> 就像员工不会背下所有规章制度，需要时翻手册。

### Skill 文件格式

```markdown
---
name: python-best-practices
description: Python 编码最佳实践
invocation: auto  # auto = 自动加载，manual = 手动加载
---

# Python 编码最佳实践

## 代码风格
- 使用 type hints
- 遵循 PEP 8
- ...

## 错误处理
- 使用具体的异常类型
- ...
```

### Skill 的加载方式

```
用户："帮我写一个 Python 脚本"
  │
  ├─ Agent 分析：需要 Python 知识
  │
  ├─ 加载 Skill：python-best-practices
  │  读取 Skill 文件内容
  │
  ├─ 注入到上下文
  │  Skill 内容作为额外上下文发送给 LLM
  │
  └─ LLM 看到 Skill 内容
     按照最佳实践编写代码
```

### Skill 的发现路径

Harness 从多个位置发现 Skill：

```
优先级从高到低：
├── .dsh/skills/          ← 项目级（最高优先级）
├── .agents/skills/       ← 项目级
├── 自定义目录            ← 可配置
├── ~/.dsh/skills/        ← 用户级
├── ~/.agents/skills/     ← 用户级
└── 内置 Skills           ← Harness 自带（最低优先级）
```

> [!note] 源码位置
> `packages/skill/skill/` — Skill 注册表
> `packages/skill/skill-filesystem/` — 文件系统 Skill 发现

---

## 2. Goal 系统 — 有状态的任务追踪

> [!tip] 类比：项目管理工具
> Goal = **Jira/Trello 上的一个任务卡片**：
>
> - 有一个明确的目标描述
> - 有状态（进行中 / 暂停 / 阻塞 / 完成）
> - 有进度追踪
> - 可以跨多个回合持续跟进

### Goal 的结构

```typescript
{
  objective: "修复登录模块的 bug",  // 目标描述
  phase: "active",                  // 状态：active | paused | blocked | complete
  revision: 3,                      // 版本号（用于并发控制）
  roundsStarted: 2,                 // 已经进行了几轮
  maxGoalRounds: 10                 // 最多允许几轮
}
```

### Goal 的状态流转

```
创建 Goal
  │
  ├─ active（活跃）→ Agent 正在努力完成
  │   │
  │   ├─ complete（完成）→ 任务完成
  │   │
  │   ├─ paused（暂停）→ Agent 暂时停下
  │   │   │
  │   │   └─ active → 恢复执行
  │   │
  │   └─ blocked（阻塞）→ 遇到无法解决的问题
  │
  └─ 达到 maxGoalRounds → 自动暂停
```

### Goal 工具

Agent 可以通过三个工具管理 Goal：

| 工具 | 作用 |
|---|---|
| `get_goal` | 查看当前 Goal 状态 |
| `create_goal` | 创建新 Goal |
| `update_goal` | 更新 Goal（修改、暂停、恢复、完成） |

### Goal Round Driver — 自动继续

> [!tip] 类比：自动提醒
> Goal Round Driver = **自动提醒你继续工作**：
>
> - Agent 完成一步后，Driver 检查 Goal 是否还活跃
> - 如果活跃，自动发送"继续工作"的消息
> - Agent 收到消息后继续执行
> - 直到 Goal 完成、阻塞、或达到轮次上限

```
Agent 完成一步
  │
  ├─ Goal Round Driver 检查
  │  Goal 状态 = active
  │  轮次 < maxGoalRounds
  │
  └─ 自动发送 continuation 消息
     Agent 收到后继续工作
     ...
     Goal 完成 → Driver 停止
```

> [!note] 源码位置
> `packages/goal/goal/` — Goal 服务
> `packages/goal/tool-goal/` — Goal 工具
> `packages/goal/goal-round-driver/` — 自动继续驱动

---

## 3. Skill + Goal 的协作

```
用户："帮我重构整个认证模块"
  │
  ├─ Agent 创建 Goal
  │  "重构认证模块"
  │
  ├─ Agent 加载相关 Skills
  │  python-best-practices
  │  authentication-patterns
  │
  ├─ Agent 分步执行
  │  Step 1: 分析现有代码 → 加载 code-review Skill
  │  Step 2: 重构 login.py → 加载 python-best-practices Skill
  │  Step 3: 重构 auth.py → 加载 python-best-practices Skill
  │  Step 4: 写测试 → 加载 testing Skill
  │
  ├─ Goal Round Driver 自动继续
  │  每步完成后自动触发下一步
  │
  └─ Goal 完成
     所有代码重构完毕
     测试通过
```

---

## 4. 其他高级系统

### Plan 模式 — 有状态的规划

```
packages/plan/ — Plan 模式作为日志状态
```

Plan 模式让 Agent 可以制定和追踪计划：

```
计划：
├── [x] 分析代码库
├── [ ] 重构 login.py
├── [ ] 重构 auth.py
├── [ ] 写测试
└── [ ] 部署
```

### Workflow 系统 — 工作流执行

```
packages/workflow/ — 工作流能力 + worker-thread provider
```

工作流让 Agent 可以执行多步骤的自动化流程：

```
工作流：
├── 触发条件：代码提交
├── 步骤 1：运行测试
├── 步骤 2：检查覆盖率
├── 步骤 3：部署到测试环境
└── 步骤 4：发送通知
```

---

## 小结

| 系统 | 一句话解释 | 类比 |
|---|---|---|
| Skill | 按需加载的知识 | 培训手册 |
| Goal | 有状态的任务追踪 | 项目任务卡片 |
| Goal Round Driver | 自动继续执行 | 自动提醒 |
| Plan | 有状态的规划 | 待办清单 |
| Workflow | 多步骤自动化 | 流程图 |

---

## 下一步

理解了高级功能后，我们来看看 Harness 的安全机制：[[14-Sandbox 与安全]]。
