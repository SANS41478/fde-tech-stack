---
title: Prompt 工程
aliases: [Prompt Engineering, 提示工程, 提示词, 提示词工程]
tags: [fde, ai, prompt, llm]
created: 2026-08-24
type: reference
domain: ai
layer: foundation
canonical: true
canonical_group: ai-prompt
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://platform.openai.com/docs/overview]
---

# Prompt 工程

> [!abstract] 定位
> **Prompt 工程** 是把客户模糊的需求翻译成模型能稳定执行的指令的艺术。FDE 不必是提示词大师，但必须能 **快速写出可复现、可校验的 prompt**——这是 AI 方案的地基。

---

## 一、为什么 FDE 必须懂 Prompt

客户说：「帮我把工单分类。」
模型不会自动知道：分几类？输出什么格式？歧义怎么办？
这些都要靠 prompt 说清楚。差的 prompt → 不稳定输出 → 没法程序消费（需要 [[Structured Output]] 兜底）。

---

## 二、核心技巧（FDE 实用版）

### 1. 角色 + 任务 + 约束（RTC）
```text
你是一个保险工单分类助手。
任务：把用户消息分为 {账单, 理赔, 投诉, 其他} 四类。
约束：只输出类别名，不要解释。
```

### 2. Few-shot（给例子）
模型通过例子学格式，比纯描述稳：
```text
输入：我的保费怎么扣多了 → 账单
输入：事故发生后怎么报案 → 理赔
输入：{用户消息} → ?
```

### 3. 链式思考（CoT）
复杂任务让模型「一步步想」：
```text
先判断用户意图，再决定类别，最后说明理由。
```

### 4. 输出格式强约束
明确要 JSON / 固定字段，配合 [[Structured Output]]：
```text
以 JSON 返回：{"category": "...", "confidence": 0-1}
```

### 5. 系统提示 vs 用户提示
- **System**：设定身份与全局规则（放 [[FastAPI]] 常量）。
- **User**：具体输入，可替换。

---

## 三、FDE 工作流中的 prompt

```text
客户模糊需求
   ↓ 抽象成角色+任务+约束
Prompt v1
   ↓ 用样例数据测
观察输出
   ↓ 不稳定？
加 few-shot / 降 temperature / 改约束
Prompt v2 → 固化
```
> 测试数据从客户真实样例里取，别用玩具数据自我安慰。

---

## 四、与结构化 / 工具的关系

- 要稳定机器可读输出 → [[Structured Output]]
- 要让模型调外部系统 → [[Tool Calling]]
- 要让模型基于私有知识回答 → [[RAG]]
- 要系统性管理模型可见的全部信息（前缀/状态/压缩）→ [[上下文工程]]

> [!tip] 经验法则
> 能用「约束输出格式」解决的，就别上复杂框架。Prompt 是 cheapest 的第一层杠杆。

---

## 五、进阶：从提示工程到上下文工程

提示工程是第一波范式，工程实践中还有几条升级路径：

- **流程驱动 > 规则堆砌**：把上百条零散规则改写成 SOP（步骤 + 条件分支 + 异常处理）。消融实验表明：保留内容但打乱组织结构，任务成功率下降 30%+。
- **业务规则细化到可执行**：模糊规则（"根据情况选择合适的计费类型"）导致行为不可预测；要写到「NEVER use X for refunds, use Y instead」的程度。生产级 Agent 的提示词由**产品经理**基于线上数据迭代，工程师负责准确编码。
- **Few-shot 的缓存纪律**：示例一旦进入上下文前部就要**字节级稳定**——按请求动态检索"最相关"示例等于每次改写前缀，缓存持续失效（见 [[KV Cache]]）。
- **按需加载**：提示词随场景膨胀到不可维护时，用 [[Agent Skills]] 渐进式披露替代单一大 prompt。
- **注入防御**：精心设计的提示词可能被外部内容劫持，见 [[提示注入]]。

---

## 五、常见坑

> [!warning]
> - **prompt 里泄露业务秘密**：别把客户敏感数据写死进 system prompt 提交给第三方。
> - **过度冗长**：长 prompt 既贵又易让模型走神，精简到必要信息。
> - **不测边界**：「其他类」、空输入、乱码都要覆盖。
> - **temperature 没设 0**：抽取/分类要可复现，却用了默认随机值。

---

相关笔记：
- [[LLM API]] —— 调用的底层
- [[Structured Output]] —— 让输出可消费
- [[Tool Calling]] —— 让模型行动
- [[RAG]] —— 注入私有知识
- [[上下文工程]] —— 系统提示词在上下文中的位置与缓存纪律
- [[Agent Skills]] —— 提示词的模块化与按需加载
- [[提示注入]] —— 提示词安全
- [[Agent 持续进化]] —— 经验如何写成指令（最小 diff 更新）
