# 第一章学习笔记：初识智能体

## 一、智能体抽象理论模型

### 1.1 四要素定义

智能体 = **Sensors（传感器）+ Actuators（执行器）+ Environment（环境）+ Autonomy（自主性）**

| 要素 | 含义 | 旅行助手中的对应 |
|---|---|---|
| 环境 | 外界世界 | API 返回数据、用户输入 |
| 传感器 | 感知渠道 | `requests.get()` 调天气/POI API |
| 执行器 | 行动工具 | `get_weather()` / `get_attraction()` |
| 自主性 | 独立决策 | LLM 自主决定调哪个工具、传什么参 |

### 1.2 PEAS 任务分析模型

描述任意 agent 任务环境：

| 维度 | 含义 | 旅行助手例子 |
|---|---|---|
| **P**erformance | 如何衡量成功 | 用户满意、推荐准确 |
| **E**nvironment | 工作环境 | 高德天气 API + 高德 POI API |
| **A**ctuators | 能做什么 | 查天气、搜景点 |
| **S**ensors | 感知什么 | API 返回的结构化 JSON、用户查询 |

### 1.3 传统智能体五层演进

```
简单反射 ──→ 基于模型 ──→ 基于目标 ──→ 基于效用 ──→ 学习型
 if-then  维护内部状态  规划达成目标  量化"好坏"  从数据中自我改进
 (恒温器) (隧道自动驾驶)  (GPS导航)   (航班比价)   (AlphaGo)
```

核心规律：越往后越**不依赖瞬时感知**，越能应对**不确定性**。传统 agent 的"大脑"是规则/搜索算法，现代 agent 的大脑换成了 LLM。

---

## 二、ReAct 范式

### 2.1 核心理念

**ReAct = Reasoning + Acting**：LLM 一边思考（Thought）一边行动（Action），观察结果（Observation）后再进入下一轮。

三要素缺一不可，最小实现就是三行伪代码：

```
while 任务未完成 and 未超最大步数:
    Thought = LLM(历史对话 + 工具定义)    # 模型推理: "我现在该做什么"
    Action = 解析 Thought 中的工具调用      # "调 get_weather(city='北京')"
    Observation = 执行工具(Action)          # 实际调用，返回 "北京: 霾, 25°C"
```

### 2.2 在 FirstAgentTest.py 中的具体形态

| 阶段 | 代码位置 | 谁负责 |
|---|---|---|
| **模型思考** | `llm.generate(...)` | LLM 基于系统提示+历史对话，输出 `Thought:... Action:...` |
| **解析工具调用** | `re.search(r"Action: (.*)")` | 正则提取工具名和参数 |
| **执行工具** | `available_tools[tool_name](**kwargs)` | Python 动态调用实际函数 |

### 2.3 ReAct 的三个阶段

| 阶段 | 负责方 | 做什么 |
|---|---|---|
| Prompt 构造 | 开发者 | 系统提示 + 工具定义 + 历史对话 → 完整 prompt |
| 思考决策 | LLM | 推理下一步该做什么，输出 Thought/Action |
| 执行反馈 | 代码 | 执行工具 → 返回结果 → 拼入历史 → 下一轮 |

### 2.4 ReAct 的核心优势

- **可解释**：每一步 Thought 可见，能追踪决策逻辑
- **可纠错**：工具失败 → 下一轮 Observation 里看到错误 → 模型自己调整策略
- **零训练**：LLM 通用推理能力天然适配
