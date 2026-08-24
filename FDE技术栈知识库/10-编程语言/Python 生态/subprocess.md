---
title: subprocess
aliases: [subprocess, 子进程, 调系统命令, 系统命令调用]
tags: [fde, python, os, automation]
created: 2026-08-24
---

# subprocess（调用系统命令）

> [!abstract] 定位
> **subprocess** 让你在 Python 里 **启动并执行外部程序 / 系统命令**，并捕获其输出。FDE 在客户环境里常遇到「只有个命令行工具能用」的情况——用它做粘合最省事。

---

## 一、为什么 FDE 要会

- 客户环境有奇怪的 **CLI 工具**：数据转换二进制、专有导出命令、老系统脚本。
- 调 [[Linux]] 命令做文件处理、压缩、[[Docker]] 操作。
- 跑 `ffmpeg`、数据库 `dump`、批处理脚本。
- 把「命令行能做的」快速包成 Python 服务/自动化（配合 [[Cron]]）。

> [!note] 与直接写 Python 的取舍
> 如果 Python 库能做，优先用库（更安全、跨平台）；只有「没有库、只有命令」时才调 subprocess——这正是 FDE 现场常见的妥协。

---

## 二、核心用法（推荐 `subprocess.run`）

```python
import subprocess, shlex

# 简单执行并捕获输出
result = subprocess.run(
    ["ls", "-l", "/data"],
    capture_output=True,      # 捕获 stdout/stderr
    text=True,                # 返回字符串而非 bytes
    timeout=30,               # 超时，防卡死
    check=True,               # 非零退出码抛异常
)
print(result.stdout)

# 管道：把 A 的输出喂给 B
p1 = subprocess.run(["cat", "a.txt"], capture_output=True, text=True)
p2 = subprocess.run(["grep", "error"], input=p1.stdout, capture_output=True, text=True)
```

---

## 三、安全要点（FDE 红线）

> [!warning] 命令注入风险
> **绝不要用 `shell=True` 拼接用户输入**：
> ```python
> # 危险！
> subprocess.run(f"convert {user_file}", shell=True)   # user_file 含 "; rm -rf /" 就完蛋
> ```
> 正确做法：**用列表传参**（参数不被 shell 解释），或严格白名单校验输入。

- 用 **参数列表** `subprocess.run([cmd, arg1, arg2])` 而非字符串。
- 用户输入必须校验/转义，最好只允许已知命令与固定参数。
- 设 `timeout`，避免外部程序挂死拖垮主进程。

---

## 四、常见坑

> [!warning]
> - **`shell=True` 注入**：如上，严重安全漏洞。
> - **不捕获输出**：管道满时子进程阻塞，主程序也卡；用 `capture_output` 或 `Popen` 正确处理。
> - **忽略返回码**：只信输出不查退出码，命令失败还当成功。
> - **路径含空格/中文**：列表传参天然安全；用字符串+shell 才易错。
> - **跨平台差异**：Windows 与 Linux 命令不同，交付注意（配合 [[Docker]] 固定环境）。

---

相关笔记：
- [[Python]] —— 所属语言
- [[Linux]] —— 常调用的命令环境
- [[Docker]] —— 容器内执行命令
- [[Cron]] —— 定时触发脚本
- [[企业系统集成]] —— 接客户奇怪系统时的兜底
