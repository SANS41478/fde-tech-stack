---
title: pandas
aliases: [pandas, DataFrame, 数据处理, 数据分析]
tags: [fde, python, data, dataframe]
created: 2026-08-24
---

# pandas

> [!abstract] 定位
> **pandas** 是 Python 的数据处理核心库，围绕 `DataFrame`（二维表）提供筛选、分组、合并、聚合等能力。FDE 经常拿到客户的脏数据（CSV / Excel / 库表），需要先清洗整理，再喂给 [[LLM API]] 或生成报表——这正是 pandas 的主场。

---

## 一、为什么 FDE 要会

- **客户数据几乎都是表格**：导出 CSV、Excel、数据库结果集。
- **AI 前处理**：把一堆行变成干净上下文，再让模型总结/分类（配合 [[RAG]]、[[Structured Output]]）。
- **快速出报表**：groupby 一下就是客户要的周报，比写 SQL 再导出快。
- **ETL 轻量实现**：小批量数据搬运与转换（见 [[ETL 与数据管道]]）。

---

## 二、核心用法

### 读入
```python
import pandas as pd
df = pd.read_csv("orders.csv")
df = pd.read_excel("report.xlsx")
# 从数据库：pd.read_sql(query, engine) 见 [[SQLAlchemy]]
```

### 筛选与选择
```python
high = df[df["amount"] > 1000]
cols = df[["id", "customer", "amount"]]
```

### 分组聚合
```python
summary = df.groupby("region")["amount"].agg(["count", "sum", "mean"])
```

### 合并
```python
merged = df.merge(customers, on="customer_id", how="left")
```

### 应用函数
```python
df["priority"] = df["amount"].apply(lambda x: "high" if x > 1000 else "low")
```

### 写出
```python
df.to_csv("clean.csv", index=False)
df.to_excel("out.xlsx", index=False)
```

---

## 三、FDE 实战模式

典型「客户数据 → AI 洞察」：
```text
read_csv / read_sql（见 [[SQLAlchemy]]）
   ↓ 清洗（去重、补空、类型转换）
   ↓ 聚合（groupby）
   ↓ 拼成文字摘要 / 结构化结果（[[Structured Output]]）
   ↓ 喂给 [[LLM API]] 或存 [[PostgreSQL]]
```

---

## 四、常见坑

> [!warning]
> - **全量进内存**：pandas 是内存计算，上百万行可能爆内存；大数据用 `chunksize` 分块或上 [[SQL]] / 数仓。
> - **SettingWithCopyWarning**：链式赋值（`df[mask]["x"]=1`）不生效，用 `.loc` 显式赋值。
> - **dtype 自动推断错**：金额被读成字符串/科学计数，读入时指定 `dtype` 或后转换。
> - **和 SQL 混淆角色**：pandas 适合「手头这份数据」的交互分析；长期/大数据走 [[SQL]] 与库。
> - **时间列没解析**：`parse_dates=[...]` 否则排序/计算按字符串。

---

相关笔记：
- [[Python]] —— 所属语言
- [[SQL]] —— 另一种数据操作范式
- [[SQLAlchemy]] —— 从库读数据进 pandas
- [[ETL 与数据管道]] —— 数据搬运大图
- [[LLM API]] —— 清洗后喂模型
