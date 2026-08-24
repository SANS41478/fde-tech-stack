---
title: Linux
aliases: [linux, Linux 命令行, 命令行, Shell, Bash]
tags: [fde, infra, linux, ops]
created: 2026-08-24
---

# Linux 与命令行

> [!abstract] 定位
> **Linux** 是 FDE 绝大多数服务的运行环境。强命令行能力意味着：拿到一台陌生服务器，你能自己排查问题、部署服务、看日志——而不是等运维。这是 FDE「能交付」的基本盘。

---

## 一、必须掌握的基础

```text
SSH             # 远程登录
Bash            # Shell 脚本
File System     # 目录/文件操作
Process         # 进程管理
Environment Variables  # 环境变量（密钥/配置）
Ports           # 端口监听
Permissions     # 权限（chmod/chown）
Logs            # 日志查看
Networking      # 网络连通性
```

---

## 二、FDE 高频命令

```bash
ls / cd              # 导航
cp / mv / rm         # 文件操作（rm 谨慎）
grep / cat / less    # 查内容
find                 # 找文件
curl / wget          # 测接口、下文件
ps / top / htop      # 看进程与资源
kill                 # 杀进程
chmod / chown        # 改权限
ss / netstat         # 看端口监听
tail -f              # 实时看日志
```

### 实战：排查服务起不来
```bash
# 1. 服务进程在吗？
ps aux | grep myapp
# 2. 端口监听吗？
ss -tlnp | grep 8000
# 3. 日志说什么？
journalctl -u myapp -n 100 --no-pager
# 4. 环境变量对吗？
printenv | grep -i token
```

---

## 三、FDE 用 Linux 做什么

- 部署 [[Docker]] 容器、跑 [[Docker Compose]]。
- 起 [[FastAPI]] / [[Node.js]] 服务（用 systemd / supervisor 守护）。
- 看生产日志、定位问题（见 [[Debugging 与可观测性]]）。
- 跑 [[Cron]] 定时任务、写 Bash 自动化脚本。
- 连 [[云平台]] 服务器做运维。

---

## 四、安全习惯

> [!warning]
> - 不用 root 日常操作；用 sudo 最小授权。
> - 密钥走环境变量 / 密钥管理，别写进脚本明文。
> - 防火墙只开必要端口。
> - `rm -rf` 三思，尤其带变量的路径。

---

## 五、常见坑

> [!warning]
> - **改了配置没生效**：忘了 reload / restart 服务。
> - **端口被占**：新服务起不来，先 `ss` 查占用。
> - **权限不足**：脚本没执行位（`chmod +x`）或文件属主错。
> - **只会在有界面的机器操作**：FDE 常在无 GUI 服务器上干活，必须习惯纯命令行。

---

相关笔记：
- [[Docker]] —— 容器化部署
- [[Debugging 与可观测性]] —— 命令行是排错主战场
- [[Cron]] —— 定时任务运行环境
- [[云平台]] —— 服务器来源
