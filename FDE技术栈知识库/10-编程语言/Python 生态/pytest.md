---
title: pytest
aliases: [pytest, py.test, 测试, Python 测试]
tags: [fde, python, testing, quality]
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

# pytest（测试）

> [!abstract] 定位
> **pytest** 是 Python 最流行的测试框架。FDE 迭代极快，测试就是「改了不崩」的保险，也是 [[CI-CD]] 自动部署前的质量闸门——没有测试，快速交付就变成了快速出 bug。

---

## 一、为什么 FDE 要会

- **快速迭代的兜底**：FDE 常改常发，测试让你敢改。
- **[[CI-CD]] 的关卡**：push 后自动跑测试，不过不部署。
- **[[Debugging 与可观测性]] 的防线**：测试最早暴露回归。
- **对外集成的稳定器**：mock 掉外部 [[LLM API]] / 客户系统，测试又快又稳。

---

## 二、核心用法

### 最基础
```python
# test_ticket.py
def test_priority():
    t = Ticket(id=1, category="billing", priority=5)
    assert t.priority <= 5
```
运行：`pytest`（自动发现 `test_*.py`）。

### Fixture（复用资源）
```python
import pytest

@pytest.fixture
def client():
    from app import app
    with app.test_client() as c:
        yield c

def test_create(client):
    r = client.post("/tickets", json={"id": 1, "category": "x"})
    assert r.status_code == 200
```

### 参数化
```python
@pytest.mark.parametrize("amt,exp", [(2000, "high"), (10, "low")])
def test_priority_level(amt, exp):
    assert level(amt) == exp
```

### Mock 外部依赖
```python
from unittest.mock import patch

def test_with_mock():
    with patch("openai.OpenAI") as mock:
        mock.return_value.chat.completions.create.return_value = fake
        # 不真调模型，测试逻辑
```

---

## 三、FDE 实战要点

- **测边界与异常**：不只 happy path，缺字段、超时、限流（429）都要覆盖。
- **外部调用全 mock**：测试里真调 [[LLM API]] / 客户 [[REST API]] 会慢且不稳定、还烧钱；用 mock/fake。
- **分层测试**：单元测试（函数级）+ 集成测试（[[FastAPI]] 端点 + 真库或测试库）。
- **覆盖率但不迷恋**：关键逻辑覆盖到位即可，别为 100% 写无意义的测试。

---

## 四、常见坑

> [!warning]
> - **只测 happy path**：异常分支没覆盖，生产才爆。
> - **测试真调外部 API**：慢、不稳定、烧钱、还可能因限流挂；务必 mock。
> - **fixture 状态泄漏**：fixture 没清理（如测试库残留），导致偶发失败；用 `yield` + teardown。
> - **慢测试阻塞迭代**：重测试移出默认套件，或标记单独跑。
> - **不接 CI**：本地过了，但没进 [[CI-CD]]，等于没闸门。

---

相关笔记：
- [[Python]] —— 所属语言
- [[FastAPI]] —— 常测的对象
- [[CI-CD]] —— 自动跑测试
- [[Debugging 与可观测性]] —— 测试的延伸
- [[LLM API]] —— 测试中需 mock 的外部依赖
