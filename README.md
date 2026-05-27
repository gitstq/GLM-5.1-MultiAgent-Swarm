# GLM-5.1 MultiAgent Swarm

基于GLM-5.1的多智能体协作系统 | Zero-dependency, 开箱即用

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)

## 🐝 项目介绍

**GLM-5.1-MultiAgent-Swarm** 是一个轻量级的多智能体协作框架，基于清华智谱GLM-5.1模型构建。它通过协调多个专业Agent（协调者、规划师、执行者、批评者、总结者）协同工作，实现复杂任务的自动化分解与执行。

### ✨ 核心亮点

- 🤖 **多Agent协作** - 5种专业角色Agent，支持层级式、并行式、顺序式执行策略
- 🚀 **零依赖设计** - 核心模块零外部依赖，开箱即用
- 🔄 **异步架构** - 全异步设计，支持高并发任务处理
- 📡 **灵活通信** - 支持消息总线、请求-响应、发布-订阅等多种通信协议
- 🔧 **易于扩展** - 模块化设计，可轻松添加自定义Agent和协议

## 🎯 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/GLM-5.1-MultiAgent-Swarm.git
cd GLM-5.1-MultiAgent-Swarm

# 安装依赖 (可选，核心功能无需依赖)
pip install requests

# 设置API密钥
export GLM_API_KEY="your-api-key-here"
```

### 5分钟快速上手

```python
import asyncio
from src.swarm import SwarmOrchestrator, Task
from src.agent import AgentRole

async def main():
    # 1. 创建Swarm编排器
    swarm = SwarmOrchestrator(name="MySwarm")
    
    # 2. 创建Agent团队 (5种角色)
    team = swarm.create_default_team()
    
    # 3. 添加任务
    task = swarm.add_task(
        description="设计并实现一个博客系统的后端API",
        task_id="blog-api"
    )
    
    # 4. 分配任务
    swarm.assign_task("blog-api", "MySwarm-planner")
    
    # 5. 执行工作流
    results = await swarm.run_workflow(
        tasks=[task],
        strategy="hierarchical"
    )
    
    print(results)

asyncio.run(main())
```

### 命令行使用

```bash
# 初始化
python -m src.cli init --name DemoSwarm

# 运行演示
python -m src.cli demo

# 执行自定义任务
python -m src.cli run "分析市场趋势并生成报告" --strategy hierarchical
```

## 📖 核心概念

### Agent角色

| 角色 | 功能 | 关键词 |
|------|------|--------|
| 🧭 Coordinator | 任务分配、进度跟踪 | 分配、协调、调度 |
| 📋 Planner | 任务拆解、计划制定 | 规划、拆解、分析 |
| ⚙️ Executor | 具体执行、结果产出 | 执行、实现、编写 |
| 🔍 Critic | 质量审查、问题发现 | 审查、检查、优化 |
| 📝 Summarizer | 结果汇总、报告生成 | 总结、汇总、整理 |

### 执行策略

- **Hierarchical (层级式)** - 按角色分阶段执行，适合复杂流程
- **Parallel (并行式)** - 多任务同时执行，适合独立任务
- **Sequential (顺序式)** - 依次执行，适合有依赖的任务

## 🛠️ API参考

### SwarmOrchestrator

```python
from src.swarm import SwarmOrchestrator, Task

# 创建编排器
swarm = SwarmOrchestrator(name="SwarmName", max_concurrent=5)

# 创建Agent
agent = swarm.create_agent(name="MyAgent", role=AgentRole.EXECUTOR)

# 添加任务
task = swarm.add_task(description="任务描述", task_id="task-1")

# 执行工作流
results = await swarm.run_workflow(tasks=[task], strategy="hierarchical")
```

### 自定义Agent

```python
from src.agent import Agent, AgentConfig, AgentRole

config = AgentConfig(
    name="CustomAgent",
    role=AgentRole.EXECUTOR,
    model="glm-5.1",
    temperature=0.7,
    capabilities=["代码编写", "问题解决"]
)

agent = Agent(config)
result = await agent.think("编写一个排序算法")
```

## 📦 项目结构

```
GLM-5.1-MultiAgent-Swarm/
├── src/                    # 核心源代码
│   ├── __init__.py
│   ├── agent.py           # Agent类定义
│   ├── swarm.py           # 编排器核心
│   ├── message.py         # 消息传递
│   ├── protocol.py        # 通信协议
│   ├── client.py          # API客户端
│   └── cli.py             # 命令行工具
├── examples/              # 示例代码
│   ├── quickstart.py      # 快速开始
│   └── advanced_usage.py  # 高级用法
├── tests/                # 测试用例
├── docs/                 # 文档
└── README.md
```

## 🔧 配置说明

### 环境变量

```bash
export GLM_API_KEY="your-api-key"
export GLM_API_BASE="https://open.bigmodel.cn/api/paas/v4"  # 可选
```

### API配置

```python
from src.client import GLMClient

client = GLMClient(
    api_key="your-key",
    api_base="https://open.bigmodel.cn/api/paas/v4",
    model="glm-5.1"
)
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 开源协议

本项目采用 MIT 开源协议。

## 🙏 致谢

- 基于 [清华智谱GLM-5.1](https://www.bigmodel.cn/) 大模型
- 灵感来源: Multi-Agent System Design Patterns

---

⭐ 如果这个项目对你有帮助，请 star 支持一下！
