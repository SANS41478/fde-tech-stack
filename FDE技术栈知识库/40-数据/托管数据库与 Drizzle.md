---
title: 托管数据库与 Drizzle
aliases: [Neon, Supabase, Drizzle ORM, 云数据库]
tags: [fde, data, database, drizzle, postgres, supabase]
created: 2026-09-14
type: reference
domain: data
layer: foundation
canonical: false
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: evergreen
sources: [https://martinfowler.com/articles/data-monolith-to-mesh.html]
---

# 托管数据库与 Drizzle

> [!abstract] 定位
> [[PostgreSQL]] 和 [[SQLAlchemy]] 讲数据库原理与 Python 落地；本篇补充 Next.js / TypeScript 项目常见的 Neon、Supabase、Drizzle 工作流，以及上线前必须处理的权限、迁移、连接和备份问题。

## 一、什么时候用托管数据库

托管数据库适合快速产品化：

- 平台负责实例、网络、备份和基础监控。
- FDE 只需获取连接字符串、定义 Schema、运行迁移。
- 开发、预览、生产可以使用不同数据库或分支。

不要把生产数据库连接字符串写入代码或提交到 Git；配置方式见 [[Node.js 项目环境与本地运行]]。

## 二、Neon / Supabase 的通用接入流程

```text
注册项目
  ↓
创建数据库
  ↓
复制连接字符串
  ↓
写入本地环境变量
  ↓
用 CLI / ORM 验证连接
  ↓
创建表并执行迁移
  ↓
建立备份和权限策略
```

验证至少包括：

- 能否连接。
- 当前用户和数据库是否正确。
- 时区、SSL、连接池是否符合环境。
- 应用账号是否只有所需权限。

## 三、Drizzle 的最小模型

```ts
import { pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";

export const tickets = pgTable("tickets", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

基本职责：

- `schema.ts`：声明表、字段、关系和约束。
- `drizzle-kit`：生成和执行迁移。
- 查询层：封装 CRUD、分页和事务。
- API 层：校验输入、检查权限、返回稳定响应。

不要直接让 AI 改线上表；Schema 变化必须生成迁移、审查 SQL，并先在预览库验证。

## 四、数据库设计底线

- 每张业务表有稳定主键。
- 关系通过外键表达，必要时加唯一约束。
- 多对多关系使用中间表。
- 业务必填字段使用 `NOT NULL`。
- 金额、时间、状态使用合适类型，不用字符串承载一切。
- 删除策略明确：级联、软删除或禁止删除。
- 租户 / 用户数据隔离策略在 Schema 和查询层同时体现。

## 五、性能与并发

### 常见陷阱

- **N+1 查询**：先查列表，再逐条查关联数据。
- **OFFSET 深分页**：页数越大越慢，稳定排序后优先游标分页。
- **先查再改**：两个请求同时通过检查，造成重复写入。
- **连接泄漏**：没有释放连接，最终耗尽连接池。
- **长事务**：事务中夹杂网络请求或用户交互，锁住资源。

解决方向：

- 用 JOIN、批量查询或预加载消除 N+1。
- 用 `(created_at, id)` 等稳定游标分页。
- 用唯一键、事务或幂等键保护写入。
- 设置连接池上限、超时和健康检查。
- 事务只包住数据库操作。

## 六、RLS 与最小权限

RLS（Row-Level Security）把「用户只能看到自己的数据」下沉到数据库层：

```text
应用漏写 where user_id = 当前用户
        ↓
数据库策略仍拒绝越权行
```

适合多租户、团队空间、用户私有数据。审查时确认：

- 所有表是否启用策略。
- SELECT、INSERT、UPDATE、DELETE 是否分别限制。
- 应用连接账号是否不能绕过策略。
- 管理后台是否使用独立、受控的高权限连接。

## 七、备份与恢复

上线前至少完成一次恢复演练：

1. 确认自动备份保留期。
2. 定期导出关键数据或快照。
3. 记录恢复到新实例的步骤。
4. 验证迁移版本与备份版本兼容。
5. 明确 RPO（最多丢多少数据）和 RTO（多久恢复）。

> [!warning] 「有备份」不等于「能恢复」
> 没有实际恢复演练、没有权限和连接信息、没有验证数据完整性，都不能算可用的备份方案。

相关笔记：

- [[PostgreSQL]]
- [[SQL]]
- [[SQLAlchemy]]
- [[REST API]]
- [[Web 用户认证与安全]]
- [[Node.js 项目环境与本地运行]]
