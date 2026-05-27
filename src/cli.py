#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行工具
"""

import sys
import argparse
import asyncio
import json
from typing import Optional

from src.swarm import SwarmOrchestrator, Task, TaskStatus
from src.agent import AgentRole
from src.client import async_chat


def print_banner():
    """打印横幅"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   🐝 GLM-5.1 MultiAgent Swarm Orchestrator 🐝          ║
    ║                                                       ║
    ║   基于GLM-5.1的多智能体协作系统                        ║
    ║   Multi-Agent Collaboration Powered by GLM-5.1        ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        description="GLM-5.1 MultiAgent Swarm - 多智能体协作系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # init命令
    init_parser = subparsers.add_parser("init", help="初始化Swarm环境")
    init_parser.add_argument("--name", default="MySwarm", help="Swarm名称")
    init_parser.add_argument("--agents", type=int, default=5, help="Agent数量")
    
    # run命令
    run_parser = subparsers.add_parser("run", help="执行任务")
    run_parser.add_argument("task", help="任务描述")
    run_parser.add_argument("--strategy", choices=["parallel", "sequential", "hierarchical"], 
                           default="hierarchical", help="执行策略")
    run_parser.add_argument("--api-key", help="GLM API密钥")
    
    # status命令
    status_parser = subparsers.add_parser("status", help="查看状态")
    
    # demo命令
    demo_parser = subparsers.add_parser("demo", help="运行演示")
    
    return parser


def cmd_init(args) -> int:
    """初始化命令"""
    print(f"🛠️  初始化 Swarm: {args.name}")
    
    swarm = SwarmOrchestrator(name=args.name)
    team = swarm.create_default_team()
    
    print(f"✅ 初始化完成!")
    print(f"   - Swarm名称: {args.name}")
    print(f"   - Agent数量: {len(team)}")
    for agent in team:
        print(f"     • {agent.name} ({agent.role.value})")
    
    # 保存配置
    config = {
        "name": args.name,
        "agents": [a.to_dict() for a in team],
    }
    
    config_path = f"{args.name.lower().replace(' ', '_')}_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"   - 配置文件: {config_path}")
    
    return 0


def cmd_run(args) -> int:
    """运行命令"""
    print(f"🚀 开始执行任务: {args.task[:50]}...")
    
    # 初始化Swarm
    swarm = SwarmOrchestrator(name="TaskSwarm")
    swarm.create_default_team()
    
    # 添加任务
    task = swarm.add_task(
        description=args.task,
        task_id="main-task",
    )
    
    # 执行
    async def run():
        results = await swarm.run_workflow(
            tasks=[task],
            strategy=args.strategy,
            request_func=async_chat,
        )
        return results
    
    results = asyncio.run(run())
    
    print("\n📊 执行结果:")
    print(json.dumps(results["summary"], indent=2, ensure_ascii=False))
    
    print("\n📝 任务结果:")
    for task_id, result in results["results"].items():
        print(f"   {task_id}: {str(result)[:100]}...")
    
    return 0


def cmd_status(args) -> int:
    """状态命令"""
    print("📊 Swarm状态")
    print("   (需要先运行 init 或 run 命令)")
    return 0


async def run_demo():
    """运行演示"""
    print("\n🎭 开始多智能体协作演示...\n")
    
    # 创建Swarm
    swarm = SwarmOrchestrator(name="DemoSwarm")
    swarm.create_default_team()
    
    # 添加演示任务
    tasks = [
        swarm.add_task("分析用户需求，设计系统架构", task_id="task-1"),
        swarm.add_task("编写核心代码模块", task_id="task-2"),
        swarm.add_task("审查代码质量和性能", task_id="task-3"),
        swarm.add_task("生成最终报告和文档", task_id="task-4"),
    ]
    
    # 分配任务
    swarm.assign_task("task-1", "DemoSwarm-planner")
    swarm.assign_task("task-2", "DemoSwarm-executor")
    swarm.assign_task("task-3", "DemoSwarm-critic")
    swarm.assign_task("task-4", "DemoSwarm-summarizer")
    
    # 执行工作流
    results = await swarm.run_workflow(
        tasks=tasks,
        strategy="hierarchical",
        request_func=async_chat,
    )
    
    # 输出结果
    print("\n" + "="*60)
    print("📋 执行报告")
    print("="*60)
    
    print(f"\n✅ 任务统计:")
    print(f"   总任务数: {results['summary']['total_tasks']}")
    print(f"   已完成: {results['summary']['completed']}")
    print(f"   失败: {results['summary']['failed']}")
    print(f"   成功率: {results['summary']['success_rate']*100:.1f}%")
    
    print(f"\n📊 任务结果:")
    for task_id, result in results["results"].items():
        status = "✓" if result else "✗"
        print(f"   {status} {task_id}: {str(result)[:60]}...")
    
    print("\n" + "="*60)


def cmd_demo(args) -> int:
    """演示命令"""
    asyncio.run(run_demo())
    return 0


def main():
    """主入口"""
    print_banner()
    
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 1
        
    commands = {
        "init": cmd_init,
        "run": cmd_run,
        "status": cmd_status,
        "demo": cmd_demo,
    }
    
    return commands.get(args.command, lambda x: 1)(args)


if __name__ == "__main__":
    sys.exit(main())
