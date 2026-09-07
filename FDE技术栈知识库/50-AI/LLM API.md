---
title: LLM API
aliases: [LLM, 大语言模型 API, 模型调用, OpenAI, Anthropic, Gemini]
tags: [fde, ai, llm, api]
created: 2026-08-24
---

# LLM API

> [!abstract] 定位
> **LLM API** 是 FDE 调用大语言模型的入口。至少理解 OpenAI、Anthropic、Gemini 三家。重点 **不是「会发一个请求」**，而是理解调用背后的成本、延迟、可靠性与可控性——这些决定了方案能不能真正交付。

---

## 一、主流提供方

| 提供方 | 特点 | FDE 关注 |
| --- | --- | --- |
| OpenAI | 生态最全、工具链成熟 | GPT-4o 系列、函数调用成熟 |
| Anthropic | 长上下文、强推理 | Claude 系列，适合长文档 |
| Gemini | 多模态、长上下文 | 谷歌生态、大窗口 |

> [!tip] FDE 策略
> 用 LiteLLM 之类的统一网关，可以在不改业务代码的前提下切换模型，避免被单家绑定。成本与能力随时权衡。

---

## 二、必须理解的底层概念

```text
Prompt         # 你给模型的指令与上下文
Context        # 模型能看到的所有信息（窗口限制）
Token          # 计费与长度单位（≈中英混合时 1 token < 1 字）
Structured Output  # 让模型返回可程序消费的结构
Streaming      # 逐 token 返回，体验更顺
Function Calling / Tool Calling  # 模型调外部工具
Temperature    # 随机性（0 稳，1 创意）
Model Selection  # 按任务选模型（快/贵/强）
Cost           # 钱：输入/输出 token 单价不同
Latency        # 延迟：用户等多久
Reliability    # 可用性：限流、宕机、重试
```

---

## 三、一个标准调用长什么样

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是工单分类助手"},
        {"role": "user", "content": text},
    ],
    temperature=0,          # 分类要稳定
    stream=True,             # 流式
)
for chunk in resp:
    print(chunk.choices[0].delta.content or "", end="")
```
> 结构化返回见 [[Structured Output]]；让模型主动调工具见 [[Tool Calling]]。

---

## 四、FDE 的四个现实约束

### 1. 成本
- 输入 token 通常比输出便宜。
- 长上下文（把整本书塞进 prompt）很贵，优先用 [[RAG]] 检索相关片段。
- 用便宜小模型做简单任务，贵大模型做难题。

### 2. 延迟
- 流式输出避免「转圈圈」空等。
- 并发调用（[[Python]] 的 asyncio）处理批量。

### 3. 可靠性
- 限流（429）要退避重试。
- 模型偶尔抽风，关键结果加校验（[[Structured Output]] + 重试）。
- 要有降级：模型挂了，系统还能兜住。

### 4. 可控性
- `temperature=0` 让分类/抽取稳定可复现。
- 用 [[Prompt 工程]] 约束输出格式与边界。

---

## 五、常见坑

> [!warning]
> - **把密钥写前端**：必须放服务端（[[FastAPI]] / [[Next.js]] API Route）。
> - **忽略 token 计费**：循环里反复塞长上下文，账单爆炸。
> - **无重试无超时**：生产环境一次抖动就 500。
> - **只用一个模型**：该小的用大，成本下不来。
> - **破坏前缀缓存**：在系统提示词里注入时间戳/动态内容，首 token 延迟与账单翻倍——见 [[KV Cache]]。

---

## 六、KV Cache 与 Prompt Cache（成本的关键杠杆）

- **Prompt Cache**：跨请求复用相同前缀的计算，缓存读取约为普通输入的 **1/10**（Anthropic/DeepSeek/GPT 系）。
- Agent 多轮调用中，上下文累积效应显著（第 1 轮发 1K token、第 3 轮发 3K，总量 6K 而非 3K）——**稳定前缀 + 历史压缩**两项优化实测可省约 30% 成本（见 [[上下文工程]]）。
- 纪律：系统提示词与工具定义一旦确定不要改；动态信息追加到末尾。

---

相关笔记：
- [[Prompt 工程]] —— 怎么写指令
- [[KV Cache]] —— 前缀缓存与成本优化
- [[上下文工程]] —— 多轮上下文的成本结构
- [[Structured Output]] —— 可控输出
- [[Tool Calling]] —— 模型调工具
- [[RAG]] / [[Embedding]] —— 降成本提准度
- [[Agent]] / [[MCP]] —— 系统化使用模型
- [[Agent 评估]] —— 模型选型维度（TTFT/吞吐/预算-能力曲线）
