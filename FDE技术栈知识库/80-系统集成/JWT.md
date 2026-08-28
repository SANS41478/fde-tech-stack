---
title: JWT
aliases: [JWT, JSON Web Token, 令牌, 无状态鉴权]
tags: [fde, integration, auth, security]
created: 2026-08-24
---

# JWT（JSON Web Token）

> [!abstract] 定位
> **JWT** 是一种 **自包含的令牌格式**：把用户身份与声明（claims）编码进 Token 本身，服务端无需查库即可校验。FDE 在自研 API 鉴权、或解析 [[OAuth]] 返回的 Token 时都会碰到它。

---

## 一、JWT 是什么

一个 JWT 由三点组成，用 `.` 分隔：
```text
Header.Payload.Signature
```
- **Header**：算法（如 HS256 / RS256）。
- **Payload**：声明（sub=用户、exp=过期、权限等）。
- **Signature**：用密钥对前两部分签名，防篡改。

> [!note] 关键点
> JWT **可被解码看到内容**（Base64），但 **不能被篡改**（签名校验）。所以别把密码等机密放 payload。

### 一·补、解码示例（claims 长什么样，值已代称）

把 JWT 中间那段 Base64 解出来，通常长这样（字段均可读，但不可改）：

```json
{
  "iss": "http://localhost:8765",   // 签发者
  "aud": "task-cli",                // 受众：令牌只允许被谁使用
  "sub": "user_abc123",            // 主体（你是谁）
  "email": "user@example.com",
  "roles": [],                     // 权限/角色声明位（分块权限字段）
  "provider": "frontend",
  "iat": 1787912280,               // 签发时间
  "exp": 1787913180                // 过期时间（iat + 900s = 15 分钟）
}
```

- `sub` / `roles`(=scope) / `exp` / `aud` 正是「限制范围只用一个字段装」的落地——资源服务器验这几项就知道「谁、能干啥、到几点、给谁用」。
- `roles:[]` 表示此账号暂未分配角色，但**槽位已就位**，框架支持细粒度授权。

> [!tip] 一个真实但匿名的端到端样本
> 某本地任务型 CLI 的 OAuth2 + JWT 实测（含登录流、令牌落盘、完整解码、15 分钟访问 / 30 天刷新），见 [[认证与授权机制]] 第九节——逐条印证本篇所有结论。

---

## 二、为什么用 JWT（无状态）

- 传统 Session：服务端存会话，多机需共享存储。
- JWT：Token 自带身份，服务端只验签名，易水平扩展。

这对 FDE 部署在 [[云平台]] / 多实例时很友好。

---

## 三、FDE 两种用法

### 1. 自研 API 鉴权
用户登录后发 JWT，之后每个请求带 `Authorization: Bearer <jwt>`：
```python
# FastAPI 依赖里校验
payload = jwt.decode(token, SECRET, algorithms=["HS256"])
user_id = payload["sub"]
```

### 2. 解析 OAuth Token
很多 [[OAuth]] 实现返回 JWT 形式的 Access Token，FDE 校验其签名与 `exp` 即可信任调用方。

---

## 四、安全要点

> [!warning]
> - **密钥别硬编码**：用环境变量 / 密钥管理（见 [[企业系统集成]] 安全）。
> - **必须验签名 + 过期**：不验就信任，等于没鉴权。
> - **别放敏感数据**：payload 可被解码。
> - **RS256 vs HS256**：多服务用非对称（RS256），公钥验签、私钥签名，避免共享密钥泄露面。

---

## 五、常见坑

> [!warning]
> - **Token 不过期 / 过长有效期**：泄露后风险窗口大，短 exp + 刷新。
> - **把 JWT 当会话黑盒存**：需要「主动登出 / 吊销」时，无状态 JWT 难即时失效，需加黑名单或短时效。
> - **算法混淆攻击**：服务端要固定预期算法，别相信 Token 自带的 `alg` 字段。
> - **前端存 JWT 不安全**：localStorage 易被 XSS 偷，敏感场景用 httpOnly Cookie。

---

相关笔记：
- [[OAuth]] —— 常返回 JWT 形式的 Token
- [[REST API]] —— Bearer Token 调接口
- [[企业系统集成]] —— 鉴权与权限总览
