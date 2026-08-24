---
title: Git
aliases: [git, Git 版本控制, GitHub, GitLab, 版本管理]
tags: [fde, engineering, git, collaboration]
created: 2026-08-24
---

# Git 与工程协作

> [!abstract] 定位
> **Git** 是分布式版本控制系统，是 FDE 管理代码、与团队/客户协作、以及让交付可回溯的基础设施。即便你是 solo FDE，Git 也是「今天改崩了能回到昨天」的保险。

---

## 一、FDE 必会基本功

```text
Git                 # 命令本身
GitHub / GitLab     # 托管与协作平台
Branch              # 分支，隔离不同改动
Commit              # 提交，原子化记录
Pull Request (PR)   # 提议合并，供评审
Merge               # 合并改动
Conflict Resolution # 冲突解决
Code Review         # 代码评审
```

---

## 二、FDE 常用流程

```text
main（稳定）
  ↓ 开 feature 分支
git checkout -b feat/crm-sync
  ↓ 改代码、提交
git commit -m "add CRM webhook handler"
  ↓ 推远程、开 PR
git push -u origin feat/crm-sync
  ↓ 评审通过 → 合并 → 触发 [[CI/CD]]
```

---

## 三、FDE 特别要注意

### 1. .gitignore 与密钥
```gitignore
.env            # 含密钥，绝不进库
node_modules/
__pycache__/
*.log
```
> 密钥泄露是大事故，见 [[企业系统集成]] 安全、[[Docker Compose]] 的 .env 处理。

### 2. 小步提交
FDE 迭代快，但提交应「一个逻辑一个 commit」，方便回滚与 review。

### 3. 分支策略要轻
不必重流程，但保持 `main` 可部署，功能在分支开发。

---

## 四、冲突解决思路

- `git status` 看哪些冲突。
- 打开文件，按 `<<<<<<<` / `=======` / `>>>>>>>` 标记手动合并。
- 验证后再 `git add` + `commit`。
- 善用 `git rebase` 整理提交历史（注意别 rebase 已推送的共享历史）。

---

## 五、常见坑

> [!warning]
> - **把 .env / 密钥提交进库**：立即轮换密钥并清理历史（git filter-repo）。
> - **长期不提交**：改一堆再提交，回滚粒度太粗。
> - **force push 公共分支**：可能覆盖他人工作，慎用 `--force`。
> - **不写清晰 commit message**：日后复盘痛苦。

---

相关笔记：
- [[CI/CD]] —— Git 事件触发部署
- [[Docker Compose]] —— .env 与 .gitignore
- [[企业系统集成]] —— 密钥安全
