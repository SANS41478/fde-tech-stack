---
title: Docker Compose
aliases: [docker-compose, Compose, 容器编排, 多容器]
tags: [fde, infra, docker, compose]
created: 2026-08-24
---

# Docker Compose

> [!abstract] 定位
> **Docker Compose** 用一个 `docker-compose.yml` 定义并启动 **多个相关容器**（前端、后端、数据库、缓存）。对 FDE 来说，它是「一条命令拉起整套系统」的终极交付形态，让客户/同事无需复杂配置就能跑起你的方案。

---

## 一、为什么需要它

单个 Docker 能跑一个服务，但 FDE 项目几乎总是多服务：
```text
Next.js 前端
FastAPI 后端
PostgreSQL 数据库
Redis 缓存
```
手动 `docker run` 四个容器、连网络、挂卷太繁琐。Compose 把它们编排成一个整体。

---

## 二、最小示例

```yaml
version: "3.9"
services:
  web:
    build: ./frontend
    ports: ["3000:3000"]
  api:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on: [db, redis]
  db:
    image: postgres:16
    volumes: ["pgdata:/var/lib/postgresql/data"]
    environment:
      - POSTGRES_PASSWORD=pass
  redis:
    image: redis:7

volumes:
  pgdata:
```

启动：
```bash
docker compose up -d      # 后台起
docker compose logs -f api # 看某个服务日志
docker compose down       # 停
```

---

## 三、FDE 关键特性

- **服务发现**：容器间用服务名互访（`api` 访问 `db:5432`），不用 IP。
- **depends_on**：控制启动顺序（注意：只等启动不等就绪，关键服务加健康检查）。
- **环境变量 / .env**：配置与密钥外置，不进仓库。
- **volumes**：数据持久化（见 [[Docker]]）。
- **一键复现**：客户拿到仓库，`docker compose up` 即得完整系统。

---

## 四、常见坑

> [!warning]
> - **depends_on 不等就绪**：db 进程起了但还没接受连接，api 先连会失败，加 `healthcheck` + `condition: service_healthy`。
> - **端口冲突**：宿主机端口被占，改映射或停占用进程（[[Linux]] 的 `ss`）。
> - **.env 进版本库**：含密钥，务必加 `.gitignore`（见 [[Git]]）。
> - **忘了停容器**：`down` 不删卷，`down -v` 才删，注意数据安全。

---

相关笔记：
- [[Docker]] —— 单容器基础
- [[PostgreSQL]] / [[Redis]] —— 常编排的服务
- [[FastAPI]] / [[Next.js]] —— 业务容器
- [[Git]] —— .env 与 .gitignore 配合
