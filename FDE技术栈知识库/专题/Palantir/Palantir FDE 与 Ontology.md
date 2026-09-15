---
title: Palantir FDE 与 Ontology
aliases: [FDE Ontology, FDE 模式, Forward Deployed Engineer Palantir, FDE 为什么需要 Ontology]
tags: [fde, palantir, ontology, business-model]
created: 2026-09-04
type: guide
domain: topic
layer: advanced
canonical: false
status: evolving
updated: 2026-09-15
sources: []
---

# Palantir FDE 与 Ontology

> [!abstract] 一句话
> Ontology 是 Palantir 的技术架构，FDE 是 Palantir 的交付模式。Ontology 解决"怎么做"，FDE 解决"谁来做、怎么落地"。两者共同构成 Palantir 的商业护城河。

---

## 一、FDE 模式与 Ontology 的关系

### FDE 卖的不是理论

Ontology 只是一套理论/策略（Object/Link/Action 建模），任何有架构师的企业都能理解。FDE 的价值不在于"教客户什么是 Ontology"，而在于：

| 价值 | 说明 |
|---|---|
| **脏活的执行能力** | 数据映射、字段对齐、edge case 处理 |
| **见过足够多案例后的判断力** | 知道什么该建、什么不该建、先做哪个 |
| **政治背书和对齐** | 外部第三方更容易推动跨部门协调 |

### 为什么企业不自己做

理论上企业完全可以自己做 Ontology。但实际困难在于：

1. **数据层面的脏活**：供应商 A 的"交货期"写天数，B 写日期，C 根本没这个字段
2. **经验缺失**：没有处理过 50 家企业的类似问题，不知道哪些坑会踩
3. **资源竞争**：Ontology 项目是"额外的"，IT 团队有日常工作
4. **KPI 不对齐**：Ontology 项目的 KPI 不在传统 IT 考核里

> [!note] FDE 的本质
> FDE 卖的是"加速器 + 经验库 + 政治背书"，而不是不可替代的技术。Palantir 的真正护城河是"20 年踩坑经验形成的行业 know-how"和"客户的切换成本"。

---

## 二、FDE 的反馈循环：Gravel Road to Pavement

FDE 模式的核心不是一次性交付，而是**从粗糙方案到标准化产品的反馈循环**：

```
客户现场（Gravel Road）
    ↓ FDE 为特定客户构建粗糙但能跑的方案
总部工程团队研究这些方案
    ↓ 找到跨客户的共性模式
标准化产品功能（Paved Highway）
    ↓ 推送给所有客户
新客户现场
    ↓ 用更成熟的产品应对，同时发现新问题
```

### 与传统咨询的区别

| 维度 | 传统咨询 | FDE |
|---|---|---|
| 交付物 | 一次性方案，做完就走 | 方案会成为产品的一部分 |
| 与产品的关系 | 独立于产品 | 反馈循环驱动产品迭代 |
| 可复用性 | 低（每个客户从零开始） | 高（共性模式被产品化） |
| 长期价值 | 有限 | 持续（客户用的是产品，不是咨询） |

---

## 三、AI 时代 FDE 模式的复兴

### 为什么 AI 时代需要 FDE

AI 系统面临和 Palantir 2003 年一样的问题：

| 挑战 | 说明 |
|---|---|
| **需求模糊** | 客户不知道 AI 能做什么，需要帮他们定义用例 |
| **环境异构** | 每家客户的数据、基础设施、业务流程都不同 |
| **落地困难** | 研究环境中能跑的模型，在生产环境中经常失败 |

这正是 FDE 模式设计要解决的问题：**在需求不明确、环境高度变异的市场中做产品发现**。

### 行业趋势

- **OpenAI**（2025 年初）：成立 FDE 团队，帮客户在生产环境中部署 AI
- **Ramp**：建立约 15 人的 FDE 团队，以 Pod 形式服务企业客户
- **a16z**：将 FDE 称为"科技行业最热门的职位"

---

## 四、AI FDE：用 AI 模拟 FDE 工作

Palantir 推出了 **AI FDE**——一个 AI Agent，模拟人类 FDE 的工作：

### AI FDE 能做什么

- 用自然语言指令执行 Foundry 操作
- 构建和维护 Ontology
- 执行数据转换、管理代码仓库
- 在 Workshop 中构建应用

### AI FDE 的意义

| 之前 | 之后 |
|---|---|
| FDE 驻场几个月，手动映射 | AI FDE 用自然语言描述，自动映射 |
| 每家客户都需要 FDE 时间 | AI FDE 可并行服务多个客户 |
| FDE 数量是瓶颈 | AI FDE 降低对人力的依赖 |

> [!warning] AI FDE 还在早期
> AI FDE 只能处理标准化的部分，复杂的业务判断和跨部门协调仍然需要人类 FDE。

---

## 五、FDE 模式的局限

> [!warning] 不要过度美化 FDE 模式
> - **成本高**：Palantir 的人天费用远高于普通咨询
> - **不可持续**：规模受限于 FDE 数量
> - **锁定客户**：Ontology 建好后，客户很难切换平台
> - **理论不新**：Ontology 是已有 30 年的理论，不是 Palantir 的发明
> - **AI 结合深度有限**：Ontology 本身不是 AI 产品，AI 是后来叠上去的

---

## 六、FDE 的核心能力矩阵

| 能力 | 在 Ontology 场景中的体现 |
|---|---|
| 数据理解 | 知道怎么把 ERP 的 300 张表映射成 15 个核心对象 |
| 架构判断 | 知道先做哪 15 个对象就能跑通第一个用例 |
| 快速原型 | 一周内出 BOM 工作流，而不是三个月 |
| 客户沟通 | 推动销售部配合财务部的数据对齐 |
| 风险控制 | 知道什么时候该复杂、什么时候该简单 |

---

## 七、相关笔记

- [[Palantir Ontology 核心概念]] —— Ontology 总览
- [[Palantir Ontology 三层架构]] —— 架构细节
- [[Palantir AIP 与 AI 集成]] —— AI 如何使用 Ontology
- [[Palantir Ontology 落地案例]] —— 真实场景
- [[FDE 角色定义]] —— FDE 是什么
- [[FDE 工作方式]] —— FDE 怎么工作
- [[FDE 能力模型]] —— FDE 能力要求
