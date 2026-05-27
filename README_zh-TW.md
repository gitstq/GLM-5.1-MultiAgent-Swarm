# GLM-5.1 MultiAgent Swarm

基於GLM-5.1的多智能體協作系統 | Zero-dependency, 開箱即用

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)

## 🐝 專案介紹

**GLM-5.1-MultiAgent-Swarm** 是一個輕量級的多智能體協作框架，基於清華智譜GLM-5.1模型構建。它透過協調多個專業Agent（協調者、規劃師、執行者、批評者、總結者）協同工作，實現複雜任務的自動化分解與執行。

### ✨ 核心亮點

- 🤖 **多Agent協作** - 5種專業角色Agent，支援層級式、並行式、順序式執行策略
- 🚀 **零依賴設計** - 核心模組零外部依賴，開箱即用
- 🔄 **異步架構** - 全異步設計，支援高並發任務處理
- 📡 **靈活通信** - 支援消息總線、請求-響應、發布-訂閱等多種通信協議
- 🔧 **易於擴展** - 模組化設計，可輕鬆添加自定義Agent和協議

## 🎯 快速開始

### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/GLM-5.1-MultiAgent-Swarm.git
cd GLM-5.1-MultiAgent-Swarm

# 安裝依賴 (可選，核心功能無需依賴)
pip install requests

# 設定API金鑰
export GLM_API_KEY="your-api-key-here"
```

### 5分鐘快速上手

```python
import asyncio
from src.swarm import SwarmOrchestrator, Task
from src.agent import AgentRole

async def main():
    # 1. 建立Swarm編排器
    swarm = SwarmOrchestrator(name="MySwarm")
    
    # 2. 建立Agent團隊 (5種角色)
    team = swarm.create_default_team()
    
    # 3. 新增任務
    task = swarm.add_task(
        description="設計並實現一個部落格系統的後端API",
        task_id="blog-api"
    )
    
    # 4. 分配任務
    swarm.assign_task("blog-api", "MySwarm-planner")
    
    # 5. 執行工作流
    results = await swarm.run_workflow(
        tasks=[task],
        strategy="hierarchical"
    )
    
    print(results)

asyncio.run(main())
```

### 命令列使用

```bash
# 初始化
python -m src.cli init --name DemoSwarm

# 執行演示
python -m src.cli demo

# 執行自定義任務
python -m src.cli run "分析市場趨勢並生成報告" --strategy hierarchical
```

## 📖 核心概念

### Agent角色

| 角色 | 功能 | 關鍵詞 |
|------|------|--------|
| 🧭 Coordinator | 任務分配、進度追蹤 | 分配、協調、排程 |
| 📋 Planner | 任務拆解、計畫制定 | 規劃、拆解、分析 |
| ⚙️ Executor | 具體執行、結果產出 | 執行、實現、編寫 |
| 🔍 Critic | 品質審查、問題發現 | 審查、檢查、最佳化 |
| 📝 Summarizer | 結果匯總、報告生成 | 總結、匯總、整理 |

### 執行策略

- **Hierarchical (層級式)** - 按角色分階段執行，適合複雜流程
- **Parallel (並行式)** - 多任務同時執行，適合獨立任務
- **Sequential (順序式)** - 依序執行，適合有依賴的任務

## 🤝 貢獻指南

歡迎提交Issue和Pull Request！

1. Fork 本倉庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送至分支 (`git push origin feature/AmazingFeature`)
5. 建立Pull Request

## 📄 開源協議

本專案採用 MIT 開源協議。

---

⭐ 如果這個專案對你有幫助，請 star 支持一下！
