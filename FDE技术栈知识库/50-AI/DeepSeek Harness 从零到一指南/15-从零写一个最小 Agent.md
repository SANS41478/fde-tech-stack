---
title: 从零写一个最小 Agent — Python 版
aliases:
  - 动手实践
  - 最小 Agent
tags:
  - deepseek-harness
  - 实践
  - python
created: 2026-08-31
---

# 从零写一个最小 Agent — Python 版

> [!tip] 目标
> 用 Python 从零写一个最小的 Agent，理解 Harness 的核心原理。代码逐行注释，确保零基础也能看懂。

---

## 1. 准备工作

### 安装 Python

```bash
# 检查是否已安装 Python
python --version

# 如果没有，去 https://python.org 下载安装
```

### 安装依赖

```bash
pip install requests
```

### 获取 API Key

你需要一个 DeepSeek API Key：
1. 访问 https://platform.deepseek.com
2. 注册账号
3. 创建 API Key

设置环境变量：

```bash
# Windows
set DEEPSEEK_API_KEY=your-api-key-here

# Mac/Linux
export DEEPSEEK_API_KEY=your-api-key-here
```

---

## 2. 最小 Agent — 逐行注释版

```python
"""
最小 Agent 实现
功能：调用 LLM，解析工具调用，执行工具，循环直到完成
"""

import json        # 处理 JSON 数据
import os          # 读取环境变量
import requests    # 发送 HTTP 请求

# ============================================================
# 第 1 步：配置
# ============================================================

# DeepSeek API 地址
API_URL = "https://api.deepseek.com/chat/completions"

# 从环境变量读取 API Key
API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# 模型名称
MODEL = "deepseek-chat"

# ============================================================
# 第 2 步：定义工具
# ============================================================

# 工具列表：告诉 LLM 有哪些工具可用
# 这和 Harness 里的 ctx.tools.register() 做的事一样
TOOLS = [
    {
        "type": "function",           # 工具类型：函数
        "function": {
            "name": "bash",           # 工具名称
            "description": "在终端中执行命令",  # 工具描述
            "parameters": {           # 参数定义
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "要执行的命令"
                    }
                },
                "required": ["command"]  # 必需参数
            }
        }
    }
]

# ============================================================
# 第 3 步：工具执行函数
# ============================================================

def execute_tool(name, arguments):
    """
    执行工具调用
    这对应 Harness 里的 tools/execute 事件
    """
    if name == "bash":
        import subprocess
        command = arguments.get("command", "")
        try:
            # 在终端执行命令，捕获输出
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30  # 30 秒超时
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return "错误：命令执行超时"
        except Exception as e:
            return f"错误：{e}"
    else:
        return f"错误：未知工具 {name}"

# ============================================================
# 第 4 步：调用 LLM
# ============================================================

def call_llm(messages, tools=None):
    """
    调用 DeepSeek API
    这对应 Harness 里的 ctx.llm.stream() 调用
    """
    # 构建请求体
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto" if tools else None
    }

    # 发送请求
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()

    # 解析响应
    data = response.json()
    return data["choices"][0]["message"]

# ============================================================
# 第 5 步：Agent Loop（核心循环）
# ============================================================

def agent_loop(user_input):
    """
    Agent 的核心循环
    这对应 Harness 里的 ReactLoopAgent
    """
    # 初始化消息历史
    # 这对应 Harness 里的 System Prompt + 历史消息
    messages = [
        {
            "role": "system",
            "content": "你是一个有用的助手，可以执行 bash 命令。"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    print(f"\n用户：{user_input}")
    print("-" * 50)

    # Agent Loop：ReAct 循环
    # 这对应 Harness 里的 kick() → turn() → step()
    max_iterations = 10  # 防止无限循环
    for iteration in range(max_iterations):
        print(f"\n--- 第 {iteration + 1} 轮 ---")

        # 调用 LLM
        print("调用 LLM...")
        response = call_llm(messages, TOOLS)

        # 检查是否有工具调用
        if response.get("tool_calls"):
            # 有工具调用 → 执行工具
            # 这对应 Harness 里的 executeToolCalls()
            for tool_call in response["tool_calls"]:
                function_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])

                print(f"工具调用：{function_name}")
                print(f"参数：{arguments}")

                # 执行工具
                result = execute_tool(function_name, arguments)
                print(f"结果：{result[:200]}...")  # 只显示前 200 字符

                # 把工具调用和结果加入消息历史
                # 这对应 Harness 里的 tool/call 和 tool/result 事件
                messages.append(response)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result
                })

        else:
            # 没有工具调用 → 直接回复
            # 这对应 Harness 里的 "completed" 状态
            print(f"\n助手：{response['content']}")
            return response["content"]

    return "达到最大迭代次数，循环结束"

# ============================================================
# 第 6 步：运行 Agent
# ============================================================

if __name__ == "__main__":
    # 测试用例
    test_cases = [
        "帮我查看当前目录有哪些文件",
        "创建一个 hello.py 文件，内容是 print('Hello, World!')",
        "运行 hello.py",
    ]

    for test in test_cases:
        agent_loop(test)
        print("\n" + "=" * 50)
```

---

## 3. 代码逐段解析

### 3.1 工具定义

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "在终端中执行命令",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "要执行的命令"
                    }
                },
                "required": ["command"]
            }
        }
    }
]
```

**与 Harness 的对应**：

| 这段代码 | Harness 中的对应 |
|---|---|
| `TOOLS` 列表 | `ctx.tools` 注册表 |
| `function.name` | 工具的唯一标识 |
| `function.description` | LLM 看到的工具描述 |
| `function.parameters` | JSON Schema（参数格式）|

### 3.2 调用 LLM

```python
def call_llm(messages, tools=None):
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto"
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]
```

**与 Harness 的对应**：

| 这段代码 | Harness 中的对应 |
|---|---|
| `messages` | 从 Session Log 推导的消息历史 |
| `tools` | 注册的工具列表 |
| `response` | LLM 的回复（assistant/message）|

### 3.3 Agent Loop

```python
for iteration in range(max_iterations):
    response = call_llm(messages, TOOLS)

    if response.get("tool_calls"):
        # 有工具调用 → 执行 → 结果加入消息 → 继续循环
        for tool_call in response["tool_calls"]:
            result = execute_tool(...)
            messages.append(response)
            messages.append({"role": "tool", "content": result})
    else:
        # 没有工具调用 → 返回结果 → 结束循环
        return response["content"]
```

**与 Harness 的对应**：

| 这段代码 | Harness 中的对应 |
|---|---|
| `for` 循环 | Agent Loop（while true）|
| `call_llm()` | step() 里的 llm.stream() |
| `execute_tool()` | executeToolCalls() |
| `messages.append()` | session.append() |
| `return` | turn/end |

---

## 4. 运行结果

```bash
python min_agent.py

用户：帮我查看当前目录有哪些文件
--------------------------------------------------

--- 第 1 轮 ---
调用 LLM...
工具调用：bash
参数：{'command': 'ls'}
结果：file1.py
file2.py
folder1/
...

--- 第 2 轮 ---
调用 LLM...

助手：当前目录有以下文件和文件夹：
- file1.py
- file2.py
- folder1/
```

---

## 5. 与 Harness 的对比

| 我们的最小 Agent | DeepSeek Harness |
|---|---|
| 直接调用 API | 通过 LLM 适配器 |
| 简单的 for 循环 | ReactLoopAgent（状态机）|
| 一个工具 | 54 个包的工具系统 |
| 无日志 | Append-Only Session Log |
| 无安全 | Sandbox + 审批系统 |
| 无记忆 | Session 持久化 |
| 单 Agent | 多 Agent 协作 |
| 无配置 | Preset + Profile + Patch |

> [!tip] 核心原理相同
> 虽然我们的是最小版本，但**核心原理完全相同**：
>
> 1. 接收消息
> 2. 组装上下文
> 3. 调用 LLM
> 4. 如果有工具调用 → 执行 → 结果放回 → 继续
> 5. 如果没有工具调用 → 返回结果 → 结束
>
> Harness 只是把这个原理工程化了，加了日志、插件、安全、多 Agent 等特性。

---

## 6. 下一步改进

如果你想继续改进这个最小 Agent，可以：

1. **添加更多工具**：文件读写、搜索等
2. **添加 Session Log**：记录每一步的事件
3. **添加错误处理**：工具执行失败时的重试
4. **添加流式输出**：逐字显示 LLM 的回复
5. **添加 Sandbox**：限制工具的执行权限

---

## 小结

通过这个最小 Agent，你理解了：

- Agent = LLM + 工具 + 循环
- 工具 = 函数 + 描述
- Agent Loop = while 循环
- 每一步：调用 LLM → 检查工具调用 → 执行 → 继续
- Harness 是这个原理的工程化实现

---

## 下一步

现在你有了实践经验，我们来总结整个学习路径：[[16-对比与总结]]。
