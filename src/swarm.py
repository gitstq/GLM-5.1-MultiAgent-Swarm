#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swarm Orchestrator - 多智能体编排器
负责任务分解、Agent协作和结果汇总
"""

import asyncio
import json
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from .agent import Agent, AgentRole, AgentConfig
from .message import Message, MessageType


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Task:
    """任务定义"""
    id: str
    description: str
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "assigned_agent": self.assigned_agent,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "result": str(self.result)[:200] if self.result else None,
            "error": self.error,
            "created_at": self.created_at,
            "duration": (
                self.completed_at - self.started_at 
                if self.started_at and self.completed_at else None
            ),
        }


class SwarmOrchestrator:
    """多智能体编排器核心类"""
    
    def __init__(
        self,
        name: str = "Swarm",
        max_concurrent: int = 5,
        timeout: int = 300,
    ):
        self.name = name
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.messages: List[Message] = []
        self.execution_log: List[Dict] = []
        
    def create_agent(
        self,
        name: str,
        role: AgentRole,
        **config_kwargs
    ) -> Agent:
        """创建Agent"""
        config = AgentConfig(name=name, role=role, **config_kwargs)
        agent = Agent(config)
        self.agents[name] = agent
        self._log(f"Agent '{name}' 创建成功，角色: {role.value}")
        return agent
    
    def create_default_team(self) -> List[Agent]:
        """创建默认团队（5种角色各一个）"""
        roles = [
            ("coordinator", AgentRole.COORDINATOR),
            ("planner", AgentRole.PLANNER),
            ("executor", AgentRole.EXECUTOR),
            ("critic", AgentRole.CRITIC),
            ("summarizer", AgentRole.SUMMARIZER),
        ]
        
        team = []
        for name_suffix, role in roles:
            agent = self.create_agent(
                name=f"{self.name}-{name_suffix}",
                role=role,
            )
            team.append(agent)
            
        self._log(f"默认团队创建完成，共 {len(team)} 个Agent")
        return team
    
    def add_task(
        self,
        description: str,
        task_id: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        **metadata
    ) -> Task:
        """添加任务"""
        if task_id is None:
            task_id = f"task-{len(self.tasks) + 1}"
            
        task = Task(
            id=task_id,
            description=description,
            dependencies=dependencies or [],
            metadata=metadata,
        )
        self.tasks[task_id] = task
        self._log(f"任务 '{task_id}' 添加成功: {description[:50]}...")
        return task
    
    def assign_task(self, task_id: str, agent_name: str) -> bool:
        """分配任务给Agent"""
        if task_id not in self.tasks:
            self._log(f"任务 '{task_id}' 不存在", level="error")
            return False
            
        if agent_name not in self.agents:
            self._log(f"Agent '{agent_name}' 不存在", level="error")
            return False
            
        task = self.tasks[task_id]
        agent = self.agents[agent_name]
        
        task.assigned_agent = agent_name
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now().timestamp()
        
        self._log(f"任务 '{task_id}' 已分配给 Agent '{agent_name}'")
        return True
    
    def execute_task(self, task: Task, agent: Agent) -> Any:
        """执行单个任务"""
        self._log(f"开始执行任务 '{task.id}'")
        
        try:
            # 获取上下文
            context = self._build_context(task)
            
            # Agent思考
            result = asyncio.run(agent.think(task.description, context))
            
            # 更新任务状态
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().timestamp()
            
            # Agent记忆
            agent.add_to_memory(f"完成任务: {task.id}", {"result": result})
            agent.state["completed_tasks"].append(task.id)
            
            self._log(f"任务 '{task.id}' 执行成功")
            return result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now().timestamp()
            self._log(f"任务 '{task.id}' 执行失败: {e}", level="error")
            return None
    
    async def execute_task_async(self, task: Task, agent: Agent) -> Any:
        """异步执行单个任务"""
        self._log(f"开始异步执行任务 '{task.id}'")
        
        try:
            context = self._build_context(task)
            result = await agent.think(task.description, context)
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().timestamp()
            
            agent.add_to_memory(f"完成任务: {task.id}", {"result": result})
            agent.state["completed_tasks"].append(task.id)
            
            self._log(f"任务 '{task.id}' 异步执行成功")
            return result
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now().timestamp()
            self._log(f"任务 '{task.id}' 异步执行失败: {e}", level="error")
            return None
    
    async def run_workflow(
        self,
        tasks: List[Task],
        strategy: str = "parallel",
        request_func: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        执行工作流
        
        Args:
            tasks: 任务列表
            strategy: 执行策略 ("parallel", "sequential", "hierarchical")
            request_func: API请求函数
        """
        self._log(f"开始执行工作流，策略: {strategy}")
        
        # 设置所有Agent的请求函数
        for agent in self.agents.values():
            if request_func:
                agent.set_request_func(request_func)
        
        # 根据策略执行
        if strategy == "parallel":
            results = await self._execute_parallel(tasks)
        elif strategy == "sequential":
            results = await self._execute_sequential(tasks)
        elif strategy == "hierarchical":
            results = await self._execute_hierarchical(tasks)
        else:
            raise ValueError(f"未知策略: {strategy}")
            
        self._log(f"工作流执行完成，成功: {sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)}")
        return self._generate_report(results)
    
    async def _execute_parallel(self, tasks: List[Task]) -> Dict:
        """并行执行"""
        # 分配任务
        for task in tasks:
            if not task.assigned_agent:
                # 自动分配给最合适的Agent
                agent = self._auto_assign(task)
                if agent:
                    self.assign_task(task.id, agent.name)
                    
        # 创建并发任务
        async_tasks = []
        for task in tasks:
            if task.assigned_agent and task.assigned_agent in self.agents:
                agent = self.agents[task.assigned_agent]
                async_tasks.append(self.execute_task_async(task, agent))
                
        # 并发执行
        results = await asyncio.gather(*async_tasks, return_exceptions=True)
        return dict(zip([t.id for t in tasks], results))
    
    async def _execute_sequential(self, tasks: List[Task]) -> Dict:
        """顺序执行"""
        results = {}
        for task in tasks:
            if task.assigned_agent and task.assigned_agent in self.agents:
                agent = self.agents[task.assigned_agent]
                result = await self.execute_task_async(task, agent)
                results[task.id] = result
            else:
                results[task.id] = None
        return results
    
    async def _execute_hierarchical(self, tasks: List[Task]) -> Dict:
        """层级执行（协调者 -> 规划师 -> 执行者 -> 批评者 -> 总结者）"""
        results = {}
        
        # 按角色分阶段执行
        for role in [AgentRole.COORDINATOR, AgentRole.PLANNER, 
                      AgentRole.EXECUTOR, AgentRole.CRITIC, AgentRole.SUMMARIZER]:
            role_agents = [a for a in self.agents.values() if a.role == role]
            if not role_agents:
                continue
                
            agent = role_agents[0]
            role_tasks = [t for t in tasks if t.status != TaskStatus.COMPLETED]
            
            for task in role_tasks:
                self.assign_task(task.id, agent.name)
                result = await self.execute_task_async(task, agent)
                results[task.id] = result
                
        return results
    
    def _auto_assign(self, task: Task) -> Optional[Agent]:
        """自动分配任务给最合适的Agent"""
        role_mapping = {
            "分配": AgentRole.COORDINATOR,
            "协调": AgentRole.COORDINATOR,
            "规划": AgentRole.PLANNER,
            "拆解": AgentRole.PLANNER,
            "执行": AgentRole.EXECUTOR,
            "编写": AgentRole.EXECUTOR,
            "分析": AgentRole.EXECUTOR,
            "审查": AgentRole.CRITIC,
            "检查": AgentRole.CRITIC,
            "总结": AgentRole.SUMMARIZER,
            "汇总": AgentRole.SUMMARIZER,
        }
        
        desc_lower = task.description.lower()
        for keyword, role in role_mapping.items():
            if keyword in desc_lower:
                agents = [a for a in self.agents.values() if a.role == role]
                if agents:
                    return agents[0]
                    
        # 默认分配给执行者
        executors = [a for a in self.agents.values() if a.role == AgentRole.EXECUTOR]
        return executors[0] if executors else None
    
    def _build_context(self, task: Task) -> Dict:
        """构建上下文"""
        context = {
            "task_history": [],
            "other_agents": [],
            "constraints": [],
        }
        
        # 添加已完成任务历史
        for t in self.tasks.values():
            if t.status == TaskStatus.COMPLETED and t.id != task.id:
                context["task_history"].append(f"- {t.id}: {t.result}")
                
        # 添加其他Agent状态
        for name, agent in self.agents.items():
            if agent.state["status"] != "idle":
                context["other_agents"].append(f"- {name}: {agent.state['status']}")
                
        # 添加依赖约束
        for dep_id in task.dependencies:
            if dep_id in self.tasks:
                dep_task = self.tasks[dep_id]
                context["constraints"].append(
                    f"依赖任务 '{dep_id}' 状态: {dep_task.status.value}"
                )
                
        return context
    
    def _generate_report(self, results: Dict) -> Dict:
        """生成执行报告"""
        completed = [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]
        failed = [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
        
        total_duration = sum(
            t.completed_at - t.started_at 
            for t in self.tasks.values() 
            if t.started_at and t.completed_at
        ) if completed else 0
        
        return {
            "summary": {
                "total_tasks": len(self.tasks),
                "completed": len(completed),
                "failed": len(failed),
                "success_rate": len(completed) / len(self.tasks) if self.tasks else 0,
                "total_duration": total_duration,
            },
            "results": {k: str(v)[:500] if v else None for k, v in results.items()},
            "execution_log": self.execution_log[-20:],  # 最近20条日志
        }
    
    def _log(self, message: str, level: str = "info"):
        """记录日志"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
        }
        self.execution_log.append(entry)
        if level == "error":
            print(f"[ERROR] {message}")
        else:
            print(f"[{self.name}] {message}")
            
    def get_status(self) -> Dict:
        """获取当前状态"""
        return {
            "name": self.name,
            "agents_count": len(self.agents),
            "tasks_total": len(self.tasks),
            "tasks_completed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
            "execution_log_size": len(self.execution_log),
        }
