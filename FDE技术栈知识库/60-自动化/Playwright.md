---
title: Playwright
aliases: [playwright, 浏览器自动化, 网页自动化, E2E]
tags: [fde, automation, browser, scraping]
created: 2026-08-24
---

# Playwright

> [!abstract] 定位
> **Playwright** 是微软出品的浏览器自动化框架，可用代码控制 Chromium / Firefox / WebKit。对 FDE 而言，它是 **没有 API 的系统也能自动化** 的利器——客户的老系统、网页后台、登录后才能看的数据，都靠它抓取与操作。

---

## 一、为什么 FDE 需要它

不是每个客户系统都提供 [[REST API]]。当对方只有网页界面时：
- 用 Playwright 登录、点击、抓取表格 → 提取数据。
- 把数据喂给 [[LLM API]] 分析或写进 [[PostgreSQL]]。
- 甚至做成 [[Agent]] 的「浏览器工具」（见 [[Tool Calling]]、[[Agent]]）。

```text
Website
   ↓ Playwright
Data Extraction
   ↓ LLM
Database
```

---

## 二、核心能力

- **选择器**：按文本、CSS、role 定位元素（优先用 role / 文本，最稳）。
- **等待**：智能等待元素出现，别用死 `sleep`。
- **输入 / 点击 / 上传 / 下载**：模拟真人操作。
- **多标签页 / iframe / 弹窗**：复杂页面也能处理。
- **无头模式（headless）**：服务器上无声运行。

### 最小示例（Python）
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://client-portal.example.com")
    page.fill("#user", user)
    page.fill("#pass", pw)
    page.click("text=登录")
    page.wait_for_selector("table#orders")
    rows = page.query_selector_all("table#orders tr")
    for r in rows:
        print(r.inner_text())
```

---

## 三、FDE 实战要点

- **稳定性第一**：用 `wait_for_*` 而非固定等待；加重试。
- **反爬 / 登录态**：用 `context` 保存 cookie，避免每次重登。
- **异常处理**：元素没出现、网络抖动要兜底（见 [[Debugging 与可观测性]]）。
- **限速**：别高频请求把客户网站打挂，尊重 robots 与合规。
- **容器化**：配合 [[Docker]] 跑无头浏览器，CI 里也能用。

---

## 四、常见坑

> [!warning]
> - **死等 sleep**：网络一慢就超时或误判，用显式等待。
> - **选择器脆弱**：用 `#id` 或易变的 class 会随改版崩，优先文本/role。
> - **只跑一次成功**：Demo 一次通 ≠ 稳定千次，必须压测重试。
> - **忽略合规**：未授权抓取敏感数据有法律风险，先确认授权。

---

相关笔记：
- [[Agent]] —— 浏览器作为工具
- [[Computer Use]] —— 通用 Agent 的 GUI 自动化（视觉定位 / SoM / 坐标缩放）
- [[事件驱动 Agent]] —— 后台任务监控与浏览器工作流固化
- [[Webhook]] / [[Cron]] —— 触发与调度
- [[ETL 与数据管道]] —— 抓取是 Extract 的一环
- [[Docker]] —— 容器化运行
