# GLM-5.1 MultiAgent Swarm

Multi-Agent Collaboration System Based on GLM-5.1 | Zero-dependency, Ready to Use

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)

## 🐝 Introduction

**GLM-5.1-MultiAgent-Swarm** is a lightweight multi-agent collaboration framework built on top of Tsinghua Zhipu AI's GLM-5.1 model. It coordinates multiple specialized Agents (Coordinator, Planner, Executor, Critic, Summarizer) to work together, enabling automated decomposition and execution of complex tasks.

### ✨ Key Features

- 🤖 **Multi-Agent Collaboration** - 5 specialized role Agents, supporting hierarchical, parallel, and sequential execution strategies
- 🚀 **Zero-Dependency Design** - Core modules with zero external dependencies, ready to use
- 🔄 **Async Architecture** - Full async design, supports high-concurrency task processing
- 📡 **Flexible Communication** - Supports message bus, request-response, publish-subscribe protocols
- 🔧 **Easy Extension** - Modular design, easily add custom Agents and protocols

## 🎯 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/gitstq/GLM-5.1-MultiAgent-Swarm.git
cd GLM-5.1-MultiAgent-Swarm

# Install dependencies (optional, core functions don't need dependencies)
pip install requests

# Set API key
export GLM_API_KEY="your-api-key-here"
```

### 5-Minute Quick Start

```python
import asyncio
from src.swarm import SwarmOrchestrator, Task
from src.agent import AgentRole

async def main():
    # 1. Create Swarm orchestrator
    swarm = SwarmOrchestrator(name="MySwarm")
    
    # 2. Create Agent team (5 roles)
    team = swarm.create_default_team()
    
    # 3. Add task
    task = swarm.add_task(
        description="Design and implement a blog system backend API",
        task_id="blog-api"
    )
    
    # 4. Assign task
    swarm.assign_task("blog-api", "MySwarm-planner")
    
    # 5. Execute workflow
    results = await swarm.run_workflow(
        tasks=[task],
        strategy="hierarchical"
    )
    
    print(results)

asyncio.run(main())
```

### CLI Usage

```bash
# Initialize
python -m src.cli init --name DemoSwarm

# Run demo
python -m src.cli demo

# Execute custom task
python -m src.cli run "Analyze market trends and generate report" --strategy hierarchical
```

## 📖 Core Concepts

### Agent Roles

| Role | Function | Keywords |
|------|----------|----------|
| 🧭 Coordinator | Task assignment, progress tracking | assign, coordinate, schedule |
| 📋 Planner | Task decomposition, planning | plan, decompose, analyze |
| ⚙️ Executor | Execute tasks, produce results | execute, implement, code |
| 🔍 Critic | Quality review, problem finding | review, check, optimize |
| 📝 Summarizer | Result aggregation, report generation | summarize, aggregate, report |

### Execution Strategies

- **Hierarchical** - Execute by role stages, suitable for complex processes
- **Parallel** - Execute multiple tasks simultaneously, suitable for independent tasks
- **Sequential** - Execute in order, suitable for dependent tasks

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

---

⭐ If this project helps you, please give it a star!
