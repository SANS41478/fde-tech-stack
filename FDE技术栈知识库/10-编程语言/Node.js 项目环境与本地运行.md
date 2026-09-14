---
title: Node.js 项目环境与本地运行
aliases: [Node 环境, pnpm, nvm, localhost, 本地开发环境]
tags: [fde, nodejs, tooling, environment, cli]
created: 2026-09-14
---

# Node.js 项目环境与本地运行

> [!abstract] 定位
> 许多「代码不能运行」不是业务代码的问题，而是 Node 版本、依赖、路径、端口或环境变量不一致。本篇把从安装到本地启动的基础链路串起来。

## 一、Node 版本与包管理

- 优先使用 Node.js **LTS**，不要在团队里混用多个大版本。
- 用 `nvm` 管理项目所需版本；在仓库中用 `.nvmrc` 或 `engines` 记录约束。
- 用 `pnpm` 管理依赖，提交 `pnpm-lock.yaml`，保证安装结果可复现。

```bash
nvm install --lts
nvm use --lts
corepack enable
corepack prepare pnpm@latest --activate
pnpm install
```

### `package.json` 与 lock 文件

- `dependencies`：运行时依赖。
- `devDependencies`：构建、测试、Lint 等开发依赖。
- `scripts`：项目命令入口。
- lock 文件：锁定完整依赖树，不应手工编辑。

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest run"
  }
}
```

## 二、项目初始化

```bash
mkdir my-app
cd my-app
pnpm create next-app@latest .
pnpm dev
```

命名建议：

- 使用英文、小写、短横线。
- 避免中文路径、空格和特殊字符。
- 项目根目录只放一个应用的配置和入口。

## 三、Terminal、PATH 与进程

- 终端当前目录决定相对路径如何解析。
- `PATH` 决定系统能否找到 `node`、`pnpm` 等命令。
- 前台进程占用终端；需要并行运行时开新终端或使用任务工具。
- 报 `command not found` 时先检查安装、PATH 和当前 shell。

常用排查：

```bash
node --version
pnpm --version
which node       # macOS / Linux
where node       # Windows
pwd              # macOS / Linux
Get-Location     # PowerShell
```

## 四、Dev、Build、Production

```text
Dev：热重载，方便修改和调试
Build：编译、类型检查、生成构建产物
Production：运行构建产物，不负责开发编译
```

不要用 `next dev` 模拟生产性能，也不要直接把源码目录当作构建产物发布。

```bash
pnpm dev
pnpm build
pnpm start
```

### 缓存排查顺序

1. 确认改动保存到了正在运行的项目。
2. 检查浏览器缓存和 Service Worker。
3. 删除 `.next` 等构建缓存后重新 Build。
4. 检查数据请求是否被框架缓存。
5. 确认环境变量改动后已重启进程。

## 五、Localhost 与端口

- `localhost` 通常指当前设备，不等于公网地址。
- 一个端口同一时间通常只能由一个服务监听。
- 前端、API、数据库可以使用不同端口；容器内端口和宿主机端口不是一回事。

```bash
pnpm dev -- --port 3001
```

遇到端口占用：

```bash
# macOS / Linux
lsof -i :3000
kill <PID>

# Windows PowerShell
Get-NetTCPConnection -LocalPort 3000
Stop-Process -Id <PID>
```

## 六、环境变量

```text
.env.local       # 本地私密配置，不提交
.env.example     # 变量名模板，可提交
```

- 服务端密钥不要使用 `NEXT_PUBLIC_` 前缀。
- 生产环境变量在部署平台单独配置。
- 变量名、类型和必填性写入 README 或技术文档。
- 修改变量后重启开发服务器。

相关笔记：

- [[Node.js]]
- [[Next.js]]
- [[TypeScript]]
- [[Linux]]
- [[Docker]]
- [[REST API]]
- [[Git]]
