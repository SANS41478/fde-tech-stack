---
title: VPS 运维与 1Panel
aliases: [云服务器运维, 1Panel, 服务器部署, VPS]
tags: [fde, infra, vps, linux, docker, operations]
created: 2026-09-14
type: reference
domain: infra
layer: foundation
canonical: false
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: moving
sources: [https://opentelemetry.io/docs/]
---

# VPS 运维与 1Panel

> [!abstract] 定位
> [[Linux]]、[[Docker]] 和 [[部署方式]] 讲基础与形态；本篇是一条从购买 VPS、初始化加固，到部署 Next.js、静态站和前后端分离应用的可复用运维路径。

## 一、VPS 选型

关注：

- 用户和数据库所在区域。
- CPU、内存、磁盘和带宽。
- IPv4、IPv6、快照和备份能力。
- 安全组、镜像、监控和账单。
- 是否需要中国大陆备案。

小型 Next.js / API Demo 通常先从低配实例开始，保留升级空间；不要为了「可能的流量」长期购买过高配置。

## 二、初始化与安全加固

```text
SSH 登录
  ↓
系统更新
  ↓
创建非 root 用户
  ↓
配置 SSH 密钥
  ↓
安全组只放行必要端口
  ↓
安装 Docker / 1Panel
  ↓
启用防火墙、Fail2Ban、备份
```

最低限度：

- 禁止密码登录，优先使用 SSH Key。
- 不让 SSH、数据库和管理面板对全网开放。
- 修改默认 SSH 端口只能降低噪音，不能替代密钥和防火墙。
- 生产密钥用服务器环境变量或密钥管理，不进镜像和仓库。
- 开启系统、Docker、应用和反向代理日志。

## 三、1Panel 与 Docker

1Panel 适合个人和小团队用可视化方式管理：

- 网站和反向代理
- Docker 应用
- PostgreSQL、Redis 等数据库
- SSL 证书
- 防火墙、计划任务和备份

容器部署必须理解：

```text
宿主机端口:容器端口
宿主机目录:容器目录（Volume）
容器名:同一 Docker 网络中的服务名
```

应用连接容器数据库时使用数据库容器名，不要在容器内写 `localhost`。

## 四、部署三种应用

### Next.js

```text
上传代码 / 拉取仓库
→ 配置环境变量
→ pnpm install
→ pnpm build
→ pnpm start
→ 反向代理到 80/443
```

内存不足时：

- 使用更小的构建并发。
- 在本地或 CI 构建后上传产物。
- 增加 Swap 作为缓冲，但不要把 Swap 当作真正内存。

### 静态网站

```text
本地 pnpm build
→ 上传 dist / out
→ 配置静态网站根目录
→ 配置 SPA fallback
→ 配置缓存与压缩
```

### 前后端分离

```text
域名 /api → 反向代理 → 后端容器
域名 /    → 反向代理 → 前端容器或静态目录
数据库    → 仅 Docker 网络可访问
```

反向代理必须处理：

- Host 和路径匹配。
- WebSocket / SSE 升级。
- 请求体大小和上传超时。
- HTTPS 终止。
- 真实客户端 IP。

## 五、日常运维

- 查看容器状态、日志和资源。
- 监控 CPU、内存、磁盘、连接数和证书有效期。
- 定期更新系统、镜像和依赖。
- 数据库和 Volume 做异地备份。
- 发布前保存镜像标签和数据库迁移版本。
- 发布失败时保留上一版本，支持回滚。

```text
变更
→ 备份
→ 预览 / 健康检查
→ 小流量发布
→ 观察日志和指标
→ 确认或回滚
```

## 六、常见问题排查

```text
域名打不开 → DNS / 安全组 / 监听端口
502         → 反向代理目标 / 容器状态 / 容器网络
页面空白    → 前端构建 / 环境变量 / 浏览器控制台
数据库连接失败 → 容器名 / 端口 / SSL / 用户权限
服务器变慢  → 内存 / Swap / 磁盘 / 日志 / 连接池
```

相关笔记：

- [[Linux]]
- [[Docker]]
- [[Docker Compose]]
- [[部署方式]]
- [[公网访问、域名与 HTTPS]]
- [[托管数据库与 Drizzle]]
- [[Debugging 与可观测性]]
