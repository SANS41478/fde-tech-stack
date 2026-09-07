---
title: MCP
aliases: [Model Context Protocol, 模型上下文协议, MCP 协议]
tags: [fde, ai, mcp, protocol]
created: 2026-08-24
---

# MCP（模型上下文协议）

> [!abstract] 定位
> **MCP（Model Context Protocol，模型上下文协议）** 是一套 **标准化「模型 ↔ 工具/数据/系统」连接方式** 的开放协议。它让 FDE 不用为每个客户系统各写一套适配，而是用统一接口把工具「插」给任意兼容的模型或客户端。

---

## 一、它解决什么痛点

没有标准时，FDE 的困境：
```text
客户 A 的 CRM  → 写一套适配
客户 B 的 ERP  → 再写一套
客户 C 的数据库 → 又一套
```
每接一个系统都从零来，重复劳动、难以复用。

MCP 的思路：把「工具 / 数据源」做成 **MCP Server**，模型/客户端（MCP Client）用统一协议调用。一次实现，处处可用。

---

## 二、核心角色

```text
MCP Client（如 IDE / Agent 宿主）
   ↕  标准协议（JSON-RPC over stdio / SSE）
MCP Server（暴露 Tools / Resources / Prompts）
   ↕
真实系统（[[PostgreSQL]] / SaaS / 文件系统 / API）
```

- **Tools**：可被模型调用的函数（对应 [[Tool Calling]]）。
- **Resources**：可被读取的数据（文件、DB 记录）。
- **Prompts**：可复用的提示模板。

---

## 三、为什么 FDE 应该关注

- **集成提速**：客户系统做成 MCP Server 后，任意兼容 Agent 直接调用，省去胶水代码。
- **可组合**：把「查 CRM」「读文档」「发 Slack」都包成 MCP Server，Agent 自由编排（见 [[Agent]]）。
- **生态红利**：越来越多工具官方提供 MCP Server，FDE 直接「即插即用」。
- **解耦**：模型 / 客户端 与 具体系统 解耦，换模型不影响工具层。

> [!tip] 与 [[Tool Calling]] 的关系
> Tool Calling 是「模型调用函数的能力」；MCP 是「把这些函数用标准协议暴露出来」的方式。MCP 让 Tool Calling 从「手写适配」升级为「标准化接入」。

---

## 四、FDE 怎么用

1. 把客户的一个系统封装成 MCP Server（暴露增查改工具）。
2. 在 Agent 宿主里连上该 Server。
3. 让模型通过统一协议调用，无需为每个系统改业务代码。

部署上，MCP Server 可随主应用一起用 [[Docker]] 容器化。

---

## 五、常见坑

> [!warning]
> - **把敏感操作无脑暴露**：MCP Server 暴露「删除/发送」工具时，权限与确认机制必须跟上（见 [[企业系统集成]] 安全）。
> - **Server 不可观测**：调用失败难排查，需日志（见 [[Debugging 与可观测性]]）。
> - **协议版本漂移**：客户端与服务端协议不一致会连不上，锁定版本。
> - **过度抽象**：简单场景直接 [[Tool Calling]] 即可，不必为上 MCP 而上 MCP。
> - **第三方 Server 的信任风险**：工具描述投毒（description 随定义进入上下文）、同名工具遮蔽、供应链攻击、凭证外流——把 description 当不可信输入审计，锁定版本拒绝静默更新（详见 [[工具设计原则]] 与 [[提示注入]]）。

---

## 六、进阶视角

- **MCP 不提供事件运行时**：它标准化「一次能力调用」，跨会话、多事件源、离线唤醒需 Agent 框架另行构建（见 [[事件驱动 Agent]]）。
- **上下文开销**：5 个 MCP Server 可引入数万 token 工具定义——延迟加载（只注入名称索引）与代理工具模式可省近一半（见 [[工具设计原则]]）。
- **MCP vs A2A vs Skills**：MCP 管 Agent↔工具互操作；A2A 管 Agent↔Agent 跨组织互操作（见 [[多 Agent 协作]]）；Skills 管能力的组织与按需披露（见 [[Agent Skills]]），Skills 也可以经 MCP 被发现和传递。

---

相关笔记：
- [[Tool Calling]] —— MCP 暴露的能力基础
- [[Agent]] —— MCP 服务的消费者
- [[企业系统集成]] —— MCP 要连接的对象
- [[工具设计原则]] —— 工具生态、延迟加载与安全
- [[Agent Skills]] —— Skills over MCP
- [[多 Agent 协作]] —— A2A 协议与 MCP 的对照
- [[Docker]] —— 容器化 MCP Server
