---
title: Docker
aliases: [docker, 容器, 容器化, Container]
tags: [fde, infra, docker, deployment]
created: 2026-08-24
type: reference
domain: infra
layer: foundation
canonical: true
canonical_group: infra-docker
status: active
updated: 2026-09-15
sources: []
---

# Docker

> [!abstract] 定位
> **Docker** 把应用及其依赖打包成 **可移植的容器**，做到「在我机器上能跑 = 在客户/服务器上也能跑」。对 FDE 来说，Docker 是交付的标准形态——它把 [[Python]] 后端、[[Next.js]] 前端、[[PostgreSQL]]、[[Redis]] 全部固化成可复现的镜像。

---

## 一、为什么 FDE 必须会 Docker

- **环境一致性**：告别「我本地能跑」。客户/生产用同一镜像。
- **快速交付**：一条命令起整套依赖，不用手装软件。
- **隔离**：不同项目依赖互不污染。
- **部署前置**：[[云平台]]、[[CI-CD|CI/CD]] 都围绕容器运转。

> [!tip] FDE 判据
> Docker 是「能写出来，也能部署出来」的分水岭能力之一。

---

## 二、必须掌握

```text
Dockerfile        # 定义镜像怎么 build
docker build      # 构建镜像
docker run        # 运行容器
docker exec       # 进容器调试
docker logs       # 看容器日志
docker ps         # 看运行中的容器
docker volume     # 数据卷（持久化）
docker network    # 容器网络
Docker Compose    # 多容器编排（见 [[Docker Compose]]）
```

### 最小 Dockerfile（FastAPI）
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 三、数据持久化要点

容器本身是临时的，数据库数据要用 **volume** 挂出来，否则容器删了数据没了：
```bash
docker run -v pgdata:/var/lib/postgresql/data postgres:16
```

---

## 四、FDE 典型部署形态

```text
Next.js    → Docker
FastAPI    → Docker
PostgreSQL → Docker
Redis      → Docker
```
多容器用 [[Docker Compose]] 一条 `docker compose up` 起来。

---

## 五、常见坑

> [!warning]
> - **把密钥打进镜像**：用 build arg / 运行时环境变量注入，镜像别含密钥。
> - **数据不挂卷**：容器重建数据丢失，数据库必须 volume。
> - **镜像巨大**：用 slim 基础镜像 + 多阶段构建，缩小体积、加快拉取。
> - **容器里跑数据库但不备份**：生产数据必须有备份策略（见 [[PostgreSQL]]）。

---

相关笔记：
- [[Docker 与 exe 容器化核心概念]] —— 概念辨析：内核 / 可移植性 / 分发 / 开销 / DLL Hell
- [[Docker Compose]] —— 多服务编排
- [[Linux]] —— 容器运行宿主
- [[云平台]] / [[CI-CD|CI/CD]] —— 镜像的归宿
- [[PostgreSQL]] / [[Redis]] —— 常容器化的组件
