---
title: Node.js 与 npm 速成 — 运行环境
aliases:
  - Node.js 基础
  - npm 入门
tags:
  - deepseek-harness
  - nodejs
  - npm
created: 2026-08-31
---

# Node.js 与 npm 速成 — 运行环境

> [!tip] 目标
> 理解 DeepSeek Harness 运行所需的环境：Node.js 是什么、npm/pnpm 是什么、package.json 是什么。

---

## 1. Node.js 是什么

> [!tip] 类比
> 浏览器 = 可以运行 JavaScript 的容器（在网页里跑 JS）
>
> Node.js = 可以在电脑上直接运行 JavaScript 的容器（不用打开浏览器）

Node.js 让你可以在**终端里**运行 JavaScript 文件：

```
# 浏览器方式：需要打开网页
# 打开浏览器 → 输入网址 → 网页里的 JS 运行

# Node.js 方式：直接在终端运行
node hello.js    ← 直接执行 JS 文件
```

> [!abstract] 技术定义
> Node.js 是一个 JavaScript 运行时环境，让 JavaScript 可以在浏览器之外执行。DeepSeek Harness 的所有代码都运行在 Node.js 上。

---

## 2. npm 和 pnpm 是什么

> [!tip] 类比
> npm/pnpm = **应用商店**
>
> 你想在手机上用某个功能 → 去应用商店下载
>
> 你想在项目里用某个功能 → 用 npm/pnpm 安装对应的包

```
你想做网页服务器
    ↓
去 npm 搜索 "express"
    ↓
npm install express    ← 下载安装
    ↓
在代码里 import express ← 使用
```

**npm vs pnpm**：

| | npm | pnpm |
|---|---|---|
| 全称 | Node Package Manager | Performant npm |
| 作用 | 安装/管理包 | 安装/管理包 |
| 区别 | 官方工具 | 更快、更省空间的替代品 |
| Harness 用哪个 | — | pnpm |

> [!note] Harness 的选择
> DeepSeek Harness 使用 **pnpm** 作为包管理器，因为 pnpm 更快且能节省磁盘空间。

---

## 3. package.json — 项目的身份证

每个 Node.js 项目都有一个 `package.json` 文件，就像项目的**身份证**：

```json
{
  "name": "@deepseek-ai/dsh-agent-loop",
  "version": "0.1.0",
  "description": "Default Agent driver over queued turns",
  "type": "module",
  "main": "lib/index.js",
  "dependencies": {
    "@deepseek-ai/cordis": "workspace:*",
    "@deepseek-ai/dsh-agent": "workspace:*",
    "@deepseek-ai/dsh-llm": "workspace:*"
  },
  "scripts": {
    "build": "tsdown",
    "test": "vitest run"
  }
}
```

**关键字段**：

| 字段 | 含义 | 类比 |
|---|---|---|
| `name` | 包的名字 | 身份证上的姓名 |
| `version` | 版本号 | 身份证上的出生日期 |
| `description` | 这个包干什么用 | 职业 |
| `type: "module"` | 使用 ES Module 格式 | 说中文还是英文 |
| `dependencies` | 需要哪些其他包 | 需要哪些工具 |
| `scripts` | 可以运行的命令 | 快捷按钮 |

> [!note] workspace:*
> 当你看到 `"@deepseek-ai/cordis": "workspace:*"`，意思是"这个依赖就在当前项目里，不需要去网上下载"。这是 monorepo（一个项目包含多个子项目）的特性。

---

## 4. monorepo — 一个项目包含多个子项目

> [!tip] 类比
> 普通项目 = 一个文件夹里有一个项目
>
> monorepo = 一个大文件夹里有很多个小项目，它们互相配合

DeepSeek Harness 是一个 monorepo：

```
deepseek-harness/           ← 根目录
├── packages/               ← 所有子项目都在这里
│   ├── core/               ← 核心包
│   │   ├── agent/          ← 一个子项目
│   │   ├── agent-loop/     ← 另一个子项目
│   │   ├── tools/          ← 又一个子项目
│   │   └── session/        ← 还有一个子项目
│   ├── llm/                ← LLM 相关包
│   ├── shell/              ← Shell 相关包
│   └── ...                 ← 还有很多
├── apps/                   ← 应用入口
│   ├── cli/                ← 命令行应用
│   ├── web/                ← Web 应用
│   └── desktop/            ← 桌面应用
├── package.json            ← 根目录的 package.json
└── pnpm-workspace.yaml     ← 告诉 pnpm 这是一个 monorepo
```

`pnpm-workspace.yaml` 文件告诉 pnpm：

```yaml
packages:
  - "packages/*/*"    # packages 目录下两级目录都是子项目
  - "apps/*"          # apps 目录下也是子项目
```

---

## 5. ESM — 模块系统

Harness 使用 **ESM**（ES Module）格式：

```typescript
// ESM 格式（Harness 使用的）
import { something } from './file.ts'    // 导入
export { something }                      // 导出

// CommonJS 格式（旧格式，Harness 不用）
const something = require('./file.js')   // 导入
module.exports = { something }           // 导出
```

> [!warning] 为什么这很重要
> Harness 的 `AGENTS.md` 明确要求"ESM everywhere"。如果你要修改 Harness 代码，必须使用 ESM 格式。

---

## 6. 构建过程

TypeScript 代码不能直接运行，需要**编译**成 JavaScript：

```
源代码（.ts 文件）
    ↓  编译（tsc 或 tsdown）
JavaScript（.js 文件）
    ↓  运行
Node.js 执行
```

Harness 的构建命令：

```bash
pnpm run build    # 编译所有包
```

构建过程：
1. `tsc`（TypeScript 编译器）生成类型声明文件（`.d.ts`）
2. `tsdown`（打包工具）生成可运行的 JavaScript 文件（`.js`）

---

## 7. 运行 Harness

从源码运行 DeepSeek Harness：

```bash
# 1. 克隆代码
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness

# 2. 安装所有依赖
pnpm install

# 3. 编译所有包
pnpm run build

# 4. 运行 Web UI
pnpm dsh web
```

每一步的作用：

| 步骤 | 作用 | 类比 |
|---|---|---|
| `git clone` | 下载源码 | 买了一套零件 |
| `pnpm install` | 安装所有依赖包 | 买了所有需要的工具 |
| `pnpm run build` | 编译 TypeScript | 按图纸组装零件 |
| `pnpm dsh web` | 启动应用 | 按下开关，开始运行 |

---

## 8. 开发时的常用命令

```bash
# 测试
pnpm run test              # 运行所有单元测试
pnpm run test:coverage     # 运行测试并检查覆盖率
pnpm run test:e2e          # 运行端到端测试（需要 API Key）

# 代码质量
pnpm run typecheck         # 检查类型错误
pnpm run lint              # 检查代码风格

# 构建
pnpm run build             # 编译所有包
pnpm run clean             # 清理编译产物

# 运行
pnpm dsh web               # 启动 Web UI
pnpm dsh --profile headless "任务"  # 执行一个任务
```

---

## 9. .env 文件 — 存放密钥

DeepSeek Harness 需要 API Key 才能调用 LLM。这些密钥存放在 `.env` 文件中：

```bash
# .env 文件内容
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com  # 可选
```

> [!warning] 安全提醒
> `.env` 文件包含敏感信息，**绝对不能提交到 Git 仓库**。Harness 的 `.gitignore` 已经排除了它。

---

## 小结

| 概念 | 一句话解释 | 类比 |
|---|---|---|
| Node.js | 在电脑上运行 JavaScript 的环境 | 浏览器之外的 JS 运行器 |
| npm/pnpm | 包管理器，安装/管理第三方库 | 应用商店 |
| package.json | 项目的身份证 | 身份证 |
| monorepo | 一个项目包含多个子项目 | 一个公司有多个部门 |
| ESM | 模块导入导出格式 | 文件间共享代码的方式 |
| 构建 | TypeScript → JavaScript | 按图纸组装零件 |
| .env | 存放 API Key 等敏感信息 | 保险箱 |

---

## 下一步

现在你了解了运行环境，接下来我们学习 Harness 的核心骨架：[[06-Cordis 插件系统]]。
