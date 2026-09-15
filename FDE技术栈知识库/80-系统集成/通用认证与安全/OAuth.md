---
title: OAuth
aliases: [OAuth, OAuth2, 授权框架, 委托授权, 第三方登录]
tags: [fde, integration, auth, security]
created: 2026-08-24
type: reference
domain: integration
layer: foundation
canonical: true
canonical_group: integration-oauth
status: active
updated: 2026-09-15
sources: []
---

# OAuth（授权框架）

> [!abstract] 定位
> **OAuth（Open Authorization）** 是一套 ** delegated 授权** 框架：让用户把「某个系统在某个权限范围内」的访问权，安全地授予你的 FDE 应用，而 **不用把账号密码告诉你**。它是接 Salesforce、Google、Slack 等 [[SaaS 集成]] 的钥匙。

---

## 一、OAuth 解决什么

没有 OAuth 时，要调客户系统得问账号密码——既不安全也不可控。
OAuth 的做法：用户跳去授权页点「允许」，你的应用拿到 **Access Token**，凭它调 API，且可限定范围、可吊销。

```text
用户 → 你的 App → 跳转授权服务器 → 用户点允许
      ← 拿到 Authorization Code ←
App 用 Code 换 Access Token + Refresh Token
App 凭 Access Token 调 API
```

---

## 二、FDE 必懂的术语

- **Authorization Code 流程**：最常用、最安全（含 PKCE 防截获），Web 应用标准。
- **Access Token**：短期有效的访问凭证（常是 [[JWT]] 或 opaque）。
- **Refresh Token**：长期凭证，用来换新的 Access Token，避免反复登录。
- **Scope**：权限范围（如 `read:orders`），最小授权原则。
- **Client ID / Secret**：你的应用身份，Secret 绝不可进前端。

### 二·补、登录流变体（浏览器 / 设备流）

OAuth 不只是「网页跳授权页」，CLI / 移动端常用这些变体：

- **浏览器登录流（CLI）**：`auth login` 打开浏览器，用户在网页点允许，本地起一个回调（如 `localhost:8765`）收回授权码，再换 Token。CLI 全程**不碰用户密码**。
- **设备流（Device Flow）**：电视/无浏览器设备显示验证码，用户去别处登录后设备轮询拿到 Token。
- **一次性令牌交换**：用别处生成的一次性 token 直接换长期凭证，免去交互。

> [!tip] 想看真实实现
> 一个匿名化的本地任务型 CLI 实测（OAuth2 浏览器流 + JWT + 混合令牌），完整收录在 [[认证与授权机制]] 第九节，可作为「教科书级」样本对照。

---

## 三、在 FDE 集成中的位置

```text
客户 CRM / SaaS
   ↓ OAuth 授权
FDE Solution（持有 Token）
   ↓ 用 Token 调 [[REST API]]
拉数据 → [[LLM API]] 分析 → 回写 / 推 [[Webhook]]
```

> [!note] 与 [[JWT]] 的关系
> OAuth 是「如何拿到授权的流程」；JWT 常是「授权后拿到的 Token 的格式」。两者常一起出现，但层次不同。

---

## 四、FDE 实战要点

- **Token 安全存储**：放服务端 / 密钥管理，别进浏览器、别进仓库（[[Git]]）。
- **自动刷新**：Access Token 过期用 Refresh Token 换，流程不能断。
- **Scope 最小**：只申请需要的权限，客户才敢授权。
- **处理撤销**：用户吊销授权后，你的 Token 失效，要有优雅降级。

---

## 五、常见坑

> [!warning]
> - **Client Secret 进前端**：等于公开，任何人可冒充你的应用。
> - **不刷新 Token**：Access Token 过期后调用全 401，体验崩。
> - **Scope 过大**：客户安全审查不通过，或引发数据越权风险。
> - **把 OAuth 当认证**：OAuth 是授权不是认证，要做登录用 OIDC（基于 OAuth 的身份层）。

---

相关笔记：
- [[JWT]] —— Token 的常见格式
- [[REST API]] —— Token 用来调接口
- [[SaaS 集成]] / [[企业系统集成]] —— OAuth 的应用场景
- [[企业系统集成]] —— 安全与权限
