# Hello-Agents Learning Progress

> 打勾规则：完成一项在这里打勾，状态：`未开始` / `进行中` / `完成`。
> 主线：快速入门 agent 应用开发，实践优先。章节文档在 `docs/`，配套代码在 `code/`，扩展材料在 `Extra-Chapter/`。
> 每章三步走：读文档 → 跑代码 → 改代码。光读不跑不算完成。
> 清单顺序与跨仓库映射见上级目录 `agent-learning-plan/LEARNING-PLAN.md`。

## Phase 1: 概念速览

### 第一章 初识智能体 — 进行中

- [ ] 读 docs/chapter1：智能体定义、类型、范式与应用
- [ ] 运行 code/chapter1/FirstAgentTest.py，看一个最小 agent 长什么样
- [ ] 用自己的话写清 chatbot / workflow / agent / multi-agent 的区别

### 第二章 智能体发展史

- [ ] 快速通读 docs/chapter2，抓住范式演进主线（符号主义 → 强化学习 → LLM 驱动）
- [ ] 跑一下 code/chapter2/ELIZA.py，感受早期对话系统

### 第三章 大语言模型基础（按需查漏，不深入算法）

- [ ] 以应用视角过 docs/chapter3：提示工程、API 调用、主流模型、模型局限
- [ ] code/chapter3 按需运行即可，不深究 Transformer 与训练细节

### 补充阅读

- [ ] 读完 Anthropic: Building effective agents
- [ ] 读完 OpenAI: A practical guide to building agents

## Phase 2: 动手核心

### 第四章 智能体经典范式构建

- [ ] 读 docs/chapter4，理解三种范式各自的设计动机
- [ ] 运行并修改 code/chapter4/ReAct.py
- [ ] 运行并修改 code/chapter4/Plan_and_solve.py
- [ ] 运行并修改 code/chapter4/Reflection.py
- [ ] 不看示例，徒手重写一个最小 ReAct loop

### 第七章 构建你的 Agent 框架

- [ ] 读 docs/chapter7，对照代码理解框架分层
- [ ] 跑通 code/chapter7/my_simple_agent.py 与 my_react_agent.py
- [ ] 给框架加一个自己的工具（参考 my_calculator_tool.py 的写法）
- [ ] 跑通 test_* 系列测试，理解每个组件为什么都要有测试

> 第六章选读：AgentScope / AutoGen / LangGraph 各过一个 demo（code/chapter6），知道定位即可，重心放在第七章自研。

## Phase 3: Harness 研究

- [ ] 读 Claude Code 官方文档（overview、tools、permissions、hooks、subagents）
- [ ] 选 learn-claude-code 或 claw0 之一：读懂目录结构，定位 agent loop、tool registry、permission gate、session store、context compaction
- [ ] 跑通其最小示例，并加一个自己的工具
- [ ] 观察一次完整 trace，解释每一步为什么发生
- [ ] 对比实验：同一个任务分别用第七章自研框架和该 harness 实现，记录差异
- 产出：可调试的 harness demo 说明（运行步骤、示例输入输出、失败记录）

## Phase 4: 进阶主题

### 第八章 记忆与检索

- [ ] 读 docs/chapter8：记忆系统分层、RAG、存储
- [ ] 跑 code/chapter8 记忆线示例（01-03）
- [ ] 跑 code/chapter8 检索线示例（04、05、10、11）
- [ ] 概念过关：chunk / embed / retrieve / rerank / 引用

### 第九章 上下文工程

- [ ] 读 docs/chapter9
- [ ] 跑 code/chapter9 的 context_builder 示例（01、02）
- [ ] 跑 code/chapter9 的 note_tool 与三日工作流示例（03、04、06）
- [ ] 补读 Extra-Chapter/Extra02-上下文工程补充知识.md

### 第十章 智能体通信协议

- [ ] 读 docs/chapter10：MCP / A2A / ANP
- [ ] 跑 code/chapter10 MCP 系列（02_Connect2MCP、05_UseMCPToolInAgent）
- [ ] 跑 code/chapter10 A2A 系列（07_SimpleA2AAgent、09_A2A_Network）
- [ ] 补读 Extra-Chapter/Extra05-AgentSkills解读.md（Skill 与 MCP 的关系）
- [ ] 写一个最小 SKILL.md（name、description、何时使用、步骤、验收标准），并加 smoke test

### 第十二章 智能体性能评估

- [ ] 读 docs/chapter12：核心指标、基准测试、评估框架
- [ ] 跑 code/chapter12 BFCL 示例（02、03）
- [ ] 跑 code/chapter12 GAIA 示例（05、06）
- [ ] 概念过关：成功率、失败分类、LLM-as-judge、回归评测

## Phase 5: 自测与查漏

- [ ] 用 Extra-Chapter/Extra01-*.md（问题总结 + 参考答案）做一轮自测：先裸答，再对答案
- [ ] 卡壳的题回对应章节补：Agent 范式 → ch4/ch7，RAG → ch8，协议 → ch10，评估 → ch12
- [ ] 再过一轮，直到 Agent / RAG / 协议 / 评估四类问题全部能顺畅作答

## Phase 6: 多智能体与综合案例

- [ ] 掌握多 agent 编排要点：角色划分、supervisor / graph 编排、职责边界与输入输出 schema、停止条件、循环与漂移处理、何时单 agent 更好
- [ ] 跑通 code/chapter14/helloagents-deepresearch 作为参考实现，理解多轮搜索 → 筛选 → 引用链路
- [ ] 亲手做一个小型多 agent 系统（research → write → review → revise）
- [ ] （可选）Browser agent：用 Playwright 或 browser-use 做一个只操作公开网页的 agent

## Phase 7: 毕业项目

- [ ] 定一个有明确用户和成功标准的任务
- [ ] 实现并选一种方式部署：CLI / Web app / bot / GitHub Action
- [ ] 补齐工程项：日志与 trace、错误重试、超时、成本上限、权限边界与人工确认
- [ ] 写 README：怎么运行、怎么配置 key、怎么扩展工具、有哪些限制
- 验收标准：别人能 clone 下来跑

## 选读（有余力再看）

- [ ] Extra-Chapter/Extra09-Agent应用开发实践踩坑与经验分享.md
- [ ] Extra-Chapter/Extra08-如何写出好的Skill.md

## 明确跳过

| 内容 | 原因 |
| --- | --- |
| 第五章 低代码平台（Coze / Dify / n8n） | 流程驱动工具，与 AI 原生 agent 主线不同，用到再看 |
| 第十一章 Agentic-RL（SFT → GRPO） | 模型训练向内容，应用开发主线不深入 |
