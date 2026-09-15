---
title: Web 用户认证与安全
aliases: [Web Auth, Better Auth, Session, RBAC, Web 安全]
tags: [fde, web, auth, security, rbac]
created: 2026-09-14
type: reference
domain: integration
layer: foundation
canonical: false
status: active
updated: 2026-09-15
sources: []
---

# Web 用户认证与安全

> [!abstract] 定位
> [[认证与授权机制]] 讲跨系统凭证和 OAuth/JWT 原理；本篇补充一个 Web 产品从注册登录到路由保护、角色权限和常见攻击面的落地方法。

## 一、认证、会话、授权三层

```text
认证 Authentication：你是谁
会话 Session：服务器如何记住你
授权 Authorization：你能访问什么
```

不要把「前端隐藏按钮」当作授权。任何页面和 API 都必须在服务端重新检查身份和权限。

## 二、用户系统最小流程

```text
注册 → 校验输入 → 创建用户 → 安全存储密码
登录 → 校验凭证 → 创建会话 → 设置安全 Cookie
访问 → 读取会话 → 检查角色/资源归属 → 返回数据
退出 → 吊销会话 / 清除 Cookie
```

优先使用成熟库（例如 Better Auth、Auth.js、Clerk、Auth0 等），不要在 FDE 项目中自行发明密码哈希、会话轮换和邮件验证。

## 三、认证方式怎么选

| 方式 | 适合 | 关键注意 |
| --- | --- | --- |
| Session Cookie | Web 应用 | 服务端保存会话，可主动吊销 |
| JWT | API、跨服务、移动端 | 短过期、验签、处理刷新和吊销 |
| OAuth / OIDC | 第三方登录、企业身份 | 区分授权和身份认证 |
| Passkey | 无密码登录 | 依赖设备和浏览器支持 |
| Magic Link | 低摩擦登录 | 邮箱链接一次性、短时有效 |
| SSO | 企业客户 | 租户、域名和身份映射要清晰 |

通常的 Web 产品优先使用 HttpOnly、Secure、SameSite Cookie 的 Session；只有在跨服务或多端需求明确时再采用 JWT。

## 四、路由与 API 保护

### 纵深防御

```text
Middleware：拦截未登录请求
页面服务端：确认用户和资源归属
API Handler：校验身份、角色、租户
数据库：RLS / 最小权限
```

Middleware 只能做快速拦截，不能替代 API 和数据库层的最终授权判断。

### RBAC 最小模型

```text
User → Membership → Role → Permission
```

例：

| 角色 | 查看 | 编辑 | 删除 | 管理成员 |
| --- | --- | --- | --- | --- |
| viewer | ✓ |  |  |  |
| editor | ✓ | ✓ |  |  |
| admin | ✓ | ✓ | ✓ | ✓ |

权限检查应同时考虑：

- 用户是否登录。
- 用户是否属于该组织 / 租户。
- 用户是否拥有该动作的权限。
- 资源是否属于当前组织。

## 五、Cookie、Token 与环境变量

- Cookie 设置 `HttpOnly`、`Secure`、合适的 `SameSite`。
- Access Token 短期有效，Refresh Token 可撤销。
- 不把 Token 放 URL、日志、错误信息或客户端可见环境变量。
- `NEXT_PUBLIC_` 变量会进入浏览器，不能放密钥。
- `.env` 不提交，`.env.example` 只保存变量名和说明。

## 六、常见 Web 攻击面

- **SQL 注入**：使用参数化查询 / ORM，不拼接用户输入。
- **XSS**：默认转义，谨慎渲染 HTML，设置 CSP。
- **CSRF**：Cookie 会话配合 SameSite、CSRF Token 或 Origin 检查。
- **CORS**：只允许明确的来源、方法和 Header，不要生产环境使用 `*`。
- **账户枚举**：登录失败提示不要暴露用户是否存在。
- **暴力破解**：登录和验证码接口限流、延迟和锁定。
- **依赖漏洞**：定期审计依赖并锁定版本。
- **敏感日志**：密码、Token、个人信息必须脱敏。

AI 应用还需额外防护：

- 工具调用前检查真实用户权限。
- 不把模型输出当作可信 SQL、Shell 或 HTML。
- 外部文档、网页和检索结果视为不可信内容。
- 关键写操作要求服务端校验和人工确认。

## 七、安全检查清单

- [ ] 未登录用户无法访问受保护页面和 API。
- [ ] API 不信任客户端传入的 `user_id` / `role`。
- [ ] 每个租户的数据访问都有服务端和数据库约束。
- [ ] 密码使用成熟库安全哈希，不自行实现。
- [ ] Cookie、Token 和密钥不出现在 URL 和日志。
- [ ] CORS、CSRF、XSS、SQL 注入都有对应防线。
- [ ] 登录、发信、上传、支付等接口有速率限制。
- [ ] 依赖、密钥和审计日志有定期检查。

相关笔记：

- [[认证与授权机制]]
- [[OAuth]]
- [[JWT]]
- [[提示注入]]
- [[托管数据库与 Drizzle]]
- [[API 产品化]]
