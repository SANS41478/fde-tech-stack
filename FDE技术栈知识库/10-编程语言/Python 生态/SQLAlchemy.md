---
title: SQLAlchemy
aliases: [SQLAlchemy, ORM, SQLAlchemy ORM, 数据库 ORM]
tags: [fde, python, database, orm]
created: 2026-08-24
type: reference
domain: language
layer: foundation
canonical: false
status: active
updated: 2026-09-15
reviewed: 2026-09-20
stability: evergreen
sources: [https://docs.python.org/3/]
---

# SQLAlchemy（ORM / 数据库）

> [!abstract] 定位
> **SQLAlchemy** 是 Python 最主流的 **ORM（对象关系映射）+ SQL 工具包**。它让你用 Python 类操作关系型数据库（主要是 [[PostgreSQL]]），既写得出可维护的数据层，又不丢掉直接写 [[SQL]] 的能力。FDE 用它把业务数据存进库、从库里读出来喂给 AI。

---

## 一、为什么 FDE 要会

- [[FastAPI]] 后端几乎标配 SQLAlchemy 做数据层。
- 比裸 SQL 字符串拼接更安全（防注入）、更易维护（模型即文档）。
- 同时支持「ORM 写法」和「核心 SQL 写法」，灵活度高于多数 ORM。
- 连接池、会话管理帮你扛住并发（见 [[System Design]]、[[asyncio]]）。

---

## 二、核心用法（2.x 风格）

### 定义模型
```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): pass

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str | None]
```

### 会话与增删查
```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg://user:pwd@localhost/app")
Session = sessionmaker(engine)

with Session() as s:
    s.add(Customer(name="ABC"))
    s.commit()
    rows = s.execute(select(Customer).where(Customer.name == "ABC")).scalars().all()
```

### 异步（配合 [[asyncio]]）
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
engine = create_async_engine("postgresql+asyncpg://...")
# async with AsyncSession(engine) as s: ...
```

---

## 三、FDE 实战要点

- **迁移用 Alembic**：模型改了，用 Alembic 生成迁移脚本，别手动改表（生产灾难）。
- **读数据进 pandas**：`pd.read_sql(select(Customer), engine)` 直接成 DataFrame（见 [[pandas]]）。
- **连接池**：默认有池，高并发注意池大小与回收，避免「连接耗尽」。
- **和 [[RAG]] 关系**：向量库（pgvector）也可用 SQLAlchemy/原生 SQL 操作。

---

## 四、常见坑

> [!warning]
> - **N+1 查询**：循环里逐个查关联对象，性能雪崩；用 `joinedload` / `selectinload` 预加载。
> - **session 生命周期乱**：跨请求复用或忘关 session 会串数据/泄漏连接；用上下文管理器。
> - **连接池耗尽**：忘了关连接或池太小，高并发时全卡；配 `pool_pre_ping`、`pool_size`。
> - **不做迁移**：直接改模型不同步库，部署即报错；用 Alembic。
> - **ORM 当银弹**：复杂报表/分析直接用 [[SQL]] 或 [[pandas]] 更高效，别硬用 ORM 拼。

---

相关笔记：
- [[Python]] —— 所属语言
- [[PostgreSQL]] —— 主要落地的数据库
- [[SQL]] —— 底层语言
- [[pandas]] —— 读库数据做分析
- [[FastAPI]] —— 常见搭配
- [[asyncio]] —— 异步会话
