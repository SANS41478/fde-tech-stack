---
title: 子 Agent 与多 Agent — 委派与协作
aliases:
  - Multi-Agent
  - 子 Agent
  - Subagent
tags:
  - deepseek-harness
  - subagent
  - multi-agent
created: 2026-08-31
---

# 子 Agent 与多 Agent — 委派与协作

> [!tip] 目标
> 理解 Harness 如何让多个 Agent 协作完成复杂任务。

---

## 1. 为什么需要子 Agent

> [!tip] 类比：项目经理分任务
> 想象你是一个**项目经理**，有一个大任务：
>
> **一个人做**：你一个人做所有事
> - 写前端代码
> - 写后端代码
> - 写测试
> - 部署
> - → 要做很久，可能做不完
>
> **分给多个人做**：你把任务分配给团队
> - 前端工程师 → 写前端
> - 后端工程师 → 写后端
> - 测试工程师 → 写测试
> - 运维工程师 → 部署
> - → 并行执行，更快完成

子 Agent 就是"团队成员"——主 Agent 可以把任务委派给它们。

---

## 2. Harness 的三种子 Agent 模式

### 2.1 Fork — 分身术

> [!tip] 类比：克隆自己
> Fork = **克隆一个自己**，继承所有记忆和能力：
>
> - 新 Agent 有完整的历史记录
> - 可以做和主 Agent 一样的事
> - 适合：需要并行处理的同类任务

```
主 Agent（处理任务 A）
  │
  ├─ Fork → 子 Agent 1（处理任务 A 的一部分）
  │
  └─ Fork → 子 Agent 2（处理任务 A 的另一部分）
```

### 2.2 Spawn — 召唤新 Agent

> [!tip] 类比：召唤助手
> Spawn = **召唤一个全新的 Agent**，从零开始：
>
> - 新 Agent 没有历史记录
> - 有独立的会话
> - 适合：完全独立的子任务

```
主 Agent（处理任务 A）
  │
  └─ Spawn → 新 Agent（处理任务 B）
             任务 B 完成后，结果返回主 Agent
```

### 2.3 ACP — 委托给其他产品

> [!tip] 类比：外包
> ACP = **把任务交给外部系统处理**：
>
> - 通过 Agent Client Protocol 通信
> - 可以是另一个 Harness 实例
> - 可以是 Claude Code、Codex 等
> - 适合：需要不同能力的子任务

```
主 Agent（处理任务 A）
  │
  └─ ACP → Claude Code（处理需要 Claude 能力的任务）
```

---

## 3. 子 Agent 的生命周期

```
主 Agent 决定委派任务
  │
  ├─ [1] 创建子 Agent
  │      fork / spawn / ACP
  │
  ├─ [2] 子 Agent 独立执行
  │      有自己的 Agent Loop
  │      有自己的 Session Log
  │      有自己的工具集
  │
  ├─ [3] 子 Agent 完成
  │      结果返回主 Agent
  │
  └─ [4] 主 Agent 继续
         把子 Agent 的结果作为上下文
         继续自己的工作
```

---

## 4. 委派深度（Delegation Depth）

> [!tip] 类比：套娃
> 子 Agent 可以再创建子 Agent，形成套娃：
>
> ```
> 主 Agent
>   └─ 子 Agent 1
>       └─ 孙 Agent 1
>           └─ 曾孙 Agent 1
>               └─ ...
> ```
>
> 但不能无限套娃！需要设置**深度限制**。

Session Header 中的 `delegationDepth` 字段追踪深度：

```typescript
{
  delegationDepth: 0,  // 主 Agent
  delegationDepth: 1,  // 子 Agent
  delegationDepth: 2,  // 孙 Agent
  // ...
}
```

**超过深度限制 → 拒绝创建**

---

## 5. 子 Agent 的工具集

子 Agent 可以有不同的工具集：

| 场景 | 工具集 |
|---|---|
| 主 Agent | 全部工具（bash、文件、搜索...） |
| 代码子 Agent | 只有代码相关工具 |
| 测试子 Agent | 只有测试相关工具 |
| 审查子 Agent | 只有读取工具（不能修改） |

> [!note] 源码位置
> `packages/subagent/` — 14 个子包，覆盖各种子 Agent 模式

---

## 6. 结果报告

子 Agent 完成后，通过 `tool-subagent-report` 向主 Agent 报告：

```
子 Agent 完成任务
  │
  ├─ 生成报告
  │  {
  │    "status": "completed",
  │    "summary": "已修复 login.py 中的 bug",
  │    "files_changed": ["login.py"],
  │    "test_results": "3 个测试通过"
  │  }
  │
  └─ 报告发送给主 Agent
     主 Agent 看到报告后决定下一步
```

---

## 7. 并行与串行

多个子 Agent 可以**并行**或**串行**执行：

```
并行（同时进行）：
  主 Agent → 子 Agent 1 ──────→ 完成
           → 子 Agent 2 ──────→ 完成
           → 子 Agent 3 ──────→ 完成
  主 Agent 等待所有子 Agent 完成

串行（一个接一个）：
  主 Agent → 子 Agent 1 → 完成
           → 子 Agent 2 → 完成
           → 子 Agent 3 → 完成
  主 Agent 依次处理每个结果
```

---

## 8. 实际例子

**场景：重构一个大型项目**

```
主 Agent（项目经理）
  │
  ├─ [1] 分析代码库
  │      → 使用搜索工具了解项目结构
  │
  ├─ [2] 制定计划
  │      → 创建 Goal：重构认证模块
  │
  ├─ [3] 委派任务
  │      ├─ Fork → 子 Agent 1：重构 login.py
  │      ├─ Fork → 子 Agent 2：重构 auth.py
  │      └─ Spawn → 子 Agent 3：写测试
  │
  ├─ [4] 等待结果
  │      子 Agent 1 → 完成
  │      子 Agent 2 → 完成
  │      子 Agent 3 → 完成
  │
  └─ [5] 整合结果
         检查所有修改
         运行测试
         提交代码
```

---

## 小结

| 概念 | 一句话解释 | 类比 |
|---|---|---|
| 子 Agent | 主 Agent 委派的任务执行者 | 团队成员 |
| Fork | 克隆主 Agent | 分身术 |
| Spawn | 创建全新 Agent | 召唤助手 |
| ACP | 委托给外部系统 | 外包 |
| 委派深度 | 限制套娃层数 | 套娃上限 |
| 结果报告 | 子 Agent 向主 Agent 汇报 | 工作汇报 |

---

## 下一步

理解了多 Agent 协作后，我们来看看如何配置不同类型的 Agent：[[12-Preset 与配置]]。
