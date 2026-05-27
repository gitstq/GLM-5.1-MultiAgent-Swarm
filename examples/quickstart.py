#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速开始脚本
"""

from src.swarm import SwarmOrchestrator, Task
from src.agent import AgentRole
from src.client import async_chat
import asyncio


async def quick_start():
    """快速开始示例"""
    print("🚀 GLM-5.1 MultiAgent Swarm 快速开始\n")
    
    # 1. 创建Swarm编排器
    swarm = SwarmOrchestrator(name="QuickStart")
    print("✓ 创建Swarm编排器成功")
    
    # 2. 创建Agent团队
    team = swarm.create_default_team()
    print(f"✓ 创建Agent团队成功 ({len(team)} 个Agent)")
    
    # 3. 添加任务
    task = swarm.add_task(
        description="分析并设计一个博客系统的技术架构",
        task_id="arch-task",
    )
    print("✓ 添加任务成功")
    
    # 4. 分配任务
    swarm.assign_task("arch-task", "QuickStart-planner")
    print("✓ 分配任务成功")
    
    # 5. 执行
    print("\n⏳ 正在执行...\n")
    results = await swarm.run_workflow(
        tasks=[task],
        strategy="hierarchical",
        request_func=async_chat,
    )
    
    # 6. 输出结果
    print("\n" + "="*60)
    print("📋 执行结果")
    print("="*60)
    print(f"\n状态: {'✅ 成功' if results['summary']['completed'] > 0 else '❌ 失败'}")
    print(f"成功率: {results['summary']['success_rate']*100:.0f}%")
    
    print("\n💡 接下来你可以:")
    print("   1. 使用 cli.py run [任务] 执行自定义任务")
    print("   2. 导入 swarm 模块构建更复杂的应用")
    print("   3. 查看 docs/ 目录了解详细文档")


def demo_without_api():
    """无API调用演示"""
    print("\n🎭 无API调用演示 (模拟模式)\n")
    
    swarm = SwarmOrchestrator(name="DemoSwarm")
    swarm.create_default_team()
    
    # 创建任务
    tasks = [
        swarm.add_task("设计用户认证模块", task_id="auth-design"),
        swarm.add_task("实现API接口", task_id="api-impl"),
        swarm.add_task("性能优化", task_id="perf-opt"),
    ]
    
    # 分配
    swarm.assign_task("auth-design", "DemoSwarm-planner")
    swarm.assign_task("api-impl", "DemoSwarm-executor")
    swarm.assign_task("perf-opt", "DemoSwarm-critic")
    
    # 执行 (不使用真实API)
    import concurrent.futures
    
    def sync_execute(task, agent):
        return agent._simulate_response(task.description)
    
    print("执行任务...\n")
    for task in tasks:
        agent = swarm.agents.get(task.assigned_agent)
        if agent:
            result = sync_execute(task, agent)
            task.result = result
            task.status = Task.COMPLETED
            print(f"✓ {task.id}: {result}")
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    print("选择模式:")
    print("1. 快速开始 (需要GLM API密钥)")
    print("2. 演示模式 (无需API)")
    
    choice = input("\n请选择 (1/2): ").strip()
    
    if choice == "1":
        asyncio.run(quick_start())
    else:
        demo_without_api()
