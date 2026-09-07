---
title: LLM API
aliases: [LLM, 大语言模型 API, 模型调用, OpenAI, Anthropic, Gemini]
tags: [fde, ai, llm, api]
created: 2026-08-24
---

# LLM API

> [!abstract] 定位
> **LLM API** 是 FDE 调用大语言模型的入口。至少理解 OpenAI、Anthropic、Gemini 三家。API 最基础的功能是「根据输入预测输出」，但在现代 Agent 架构中核心已升级为 **指令遵循（Instruction Following）**——模型不仅要「接话」，更要精准「做事」。FDE 的重点 **不是「会发一个请求」**，而是理解调用背后的成本、延迟、可靠性与可控性——这些决定了方案能不能真正交付。

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

### 三大角色与核心要素

| 要素 | 作用 |
| --- | --- |
| **System Prompt** | 设定模型的角色、语气和全局规则 |
| **User / Assistant 轮换** | 维护多轮对话的上下文逻辑 |
| **Tools / Function Calling** | 模型不直接回答，而是输出结构化 JSON 指令调用外部 API（见 [[Tool Calling]]） |

### 基础概念速查

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

## 三、核心采样参数：指挥模型「性格」的旋钮

这些参数是开发者唯一能直接「指挥」模型性格的旋钮，决定了模型如何从海量概率中挑选下一个词。

| 参数 | 作用机制 | 推荐取值 |
| --- | --- | --- |
| **Temperature（温度）** | 值越低（趋近 0），越倾向选概率最高的词，输出**确定且保守**（适合代码生成、分类、翻译）；值越高（趋近 1），随机性越大，输出**多样且富有创意**（适合写作） | 0.1 ~ 0.9 |
| **Top-P（核采样）** | 限制候选词的总概率累积和，与 Temperature 配合使用，精细控制词汇池大小 | 0.9 ~ 1.0 |
| **Max Tokens** | 限制输出文本的最大长度，同时直接影响本次调用的计费成本 | 按任务设定 |

> [!tip] FDE 实践
> 分类、抽取、代码生成用 `temperature=0` 保证可复现；创意写作用 0.7~0.9。二者一般 **调一个即可**，同时大幅调整两个参数反而难排查问题。

---

## 四、Token 计费：成本结构的核心规律

Token 是模型识别的最小语义单元（英文一个单词通常 1 个 Token，中文一个词可能拆成 1~2 个 Token）。

- API 返回的 `usage` 字段包含 `prompt_tokens`（输入）与 `completion_tokens`（输出）。
- **核心规律：输出 Token 的价格通常是输入 Token 的 2~10 倍**——生成是逐 token 串行计算，远比并行理解昂贵耗时。
- 呼应 [[KV Cache]]：缓存命中的输入 token 约为普通输入的 1/10，而输出永远全价——**能「检索/复用」的别让模型「生成」**。

---

## 五、一个标准调用长什么样

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

## 六、底层格式 vs 上层 API：两层映射的「减震器」架构

### 1. 底层：模型训练时「自带」的物理格式（强制性）

模型微调（Instruction Tuning）阶段，训练数据本身就强制包含特定分隔符（如 Llama 3 官方模板要求输入包裹为特定结构，详见 [[KV Cache]] 的 Chat Template 章节）。

- 模型的神经网络权重已经「死记硬背」了这种角色分区。**不按该模型的特定底层格式传参，模型根本听不懂指令**，推理结果完全错乱。
- 不同厂商底层模板完全不同（`<|im_start|>` vs `[INST]`）。

### 2. 上层：API 服务层的统一封装（兼容性）

客户端发送标准化的 `{"role": "system", "content": "..."}` JSON，API 服务层负责翻译成该模型自己的物理格式。

> [!important] 这层映射不是累赘，而是生态的「减震器」
> 它允许底层模型疯狂内卷（各自改架构、换模板），上层应用毫发无伤——开发者可随时更换性价比最高的底层模型，而无需重写全量业务代码。

### 3. Tools 是「纯规范」，并非模型自带

- 原始裸模型只会吐文字，不会吐 JSON 指令。Tools 是 API 服务层在 System Prompt 最底层**偷偷注入的「隐形工具使用说明书」**，并配合 **约束采样（Constrained Decoding）** 在 GPU 层面强行让模型只输出合法 JSON，不带半个多余字符。
- **核心意义：API 统一的是「语文」（动作描述语法），而不是「职业」（具体工具）**。无论工具是查天气还是订机票，发给模型的 JSON 骨架都是统一的 `{"name": "...", "arguments": "{...}"}`。

---

## 七、FDE 的四个现实约束

### 1. 成本
- 输出 token 通常比输入贵 2~10 倍（见「四、Token 计费」），让模型「少生成」比「少输入」更省钱。
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

## 八、常见坑

> [!warning]
> - **把密钥写前端**：必须放服务端（[[FastAPI]] / [[Next.js]] API Route）。
> - **忽略 token 计费**：循环里反复塞长上下文，账单爆炸。
> - **无重试无超时**：生产环境一次抖动就 500。
> - **只用一个模型**：该小的用大，成本下不来。
> - **破坏前缀缓存**：在系统提示词里注入时间戳/动态内容，首 token 延迟与账单翻倍——见 [[KV Cache]]。

---

## 九、KV Cache 与 Prompt Cache（成本的关键杠杆）

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
