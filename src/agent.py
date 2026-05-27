#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心Agent类定义
支持多种角色和专业能力
"""

import json
import time
from enum import Enum
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field


class AgentRole(Enum):
    """Agent角色枚举"""
    COORDINATOR = "coordinator"      # 协调者 - 负责任务分配和进度跟踪
    PLANNER = "planner"             # 规划师 - 负责任务拆解和执行计划
    EXECUTOR = "executor"           # 执行者 - 负责具体任务执行
    CRITIC = "critic"               # 批评者 - 负责质量检查和问题发现
    SUMMARIZER = "summarizer"       # 总结者 - 负责结果汇总和输出


@dataclass
class AgentConfig:
    """Agent配置"""
    name: str
    role: AgentRole
    model: str = "glm-5.1"
    temperature: float = 0.7
    max_tokens: int = 4096
    system_prompt: str = ""
    capabilities: List[str] = field(default_factory=list)
    api_key: Optional[str] = None
    api_base: str = "https://open.bigmodel.cn/api/paas/v4"
    
    def __post_init__(self):
        if not self.system_prompt:
            role_prompts = {
                AgentRole.COORDINATOR: "你是一个任务协调者，负责协调多个Agent的工作，分配任务，跟踪进度。",
                AgentRole.PLANNER: "你是一个规划师，负责将复杂任务拆解为可执行的子任务，制定执行计划。",
                AgentRole.EXECUTOR: "你是一个执行者，负责执行具体的任务，产生高质量的结果。",
                AgentRole.CRITIC: "你是一个批评者，负责审查工作成果，发现问题并提出改进建议。",
                AgentRole.SUMMARIZER: "你是一个总结者，负责将多个Agent的工作成果汇总成最终输出。",
            }
            self.system_prompt = role_prompts.get(self.role, "你是一个AI助手。")
        if not self.capabilities:
            capability_map = {
                AgentRole.COORDINATOR: ["任务分配", "进度跟踪", "冲突协调", "资源调度"],
                AgentRole.PLANNER: ["任务拆解", "计划制定", "依赖分析", "风险评估"],
                AgentRole.EXECUTOR: ["代码编写", "数据分析", "文档生成", "问题解决"],
                AgentRole.CRITIC: ["质量审查", "问题发现", "优化建议", "错误检测"],
                AgentRole.SUMMARIZER: ["结果汇总", "报告生成", "格式整理", "关键提取"],
            }
            self.capabilities = capability_map.get(self.role, [])


class Agent:
    """核心Agent类"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.role = config.role
        self.state: Dict[str, Any] = {
            "status": "idle",
            "current_task": None,
            "completed_tasks": [],
            "messages": [],
            "memory": [],
        }
        self._request_func: Optional[Callable] = None
        
    def set_request_func(self, func: Callable):
        """设置请求函数"""
        self._request_func = func
        
    def update_state(self, **kwargs):
        """更新Agent状态"""
        self.state.update(kwargs)
        
    def add_message(self, message: Dict):
        """添加消息到历史"""
        self.state["messages"].append({
            **message,
            "timestamp": time.time(),
        })
        
    def add_to_memory(self, content: str, metadata: Optional[Dict] = None):
        """添加到记忆"""
        self.state["memory"].append({
            "content": content,
            "metadata": metadata or {},
            "timestamp": time.time(),
        })
        
    async def think(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Agent思考过程"""
        self.state["status"] = "thinking"
        
        # 构建完整提示
        full_prompt = self._build_prompt(prompt, context)
        
        # 调用API
        if self._request_func:
            response = await self._request_func(
                prompt=full_prompt,
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                api_key=self.config.api_key,
                api_base=self.config.api_base,
            )
        else:
            # 模拟响应（当没有API时）
            response = self._simulate_response(prompt)
            
        self.state["status"] = "idle"
        return response
        
    def _build_prompt(self, prompt: str, context: Optional[Dict] = None) -> str:
        """构建完整提示"""
        parts = [f"角色: {self.config.system_prompt}"]
        parts.append(f"专业能力: {', '.join(self.config.capabilities)}")
        
        if context:
            if "task_history" in context:
                parts.append(f"\n任务历史:\n{context['task_history']}")
            if "other_agents" in context:
                parts.append(f"\n其他Agent状态:\n{context['other_agents']}")
            if "constraints" in context:
                parts.append(f"\n约束条件:\n{context['constraints']}")
                
        parts.append(f"\n当前任务: {prompt}")
        return "\n\n".join(parts)
        
    def _simulate_response(self, prompt: str) -> str:
        """模拟响应（用于演示）"""
        responses = {
            AgentRole.COORDINATOR: f"[协调者 {self.name}] 已接收任务，正在分析并分配...",
            AgentRole.PLANNER: f"[规划师 {self.name}] 正在拆解任务，制定执行计划...",
            AgentRole.EXECUTOR: f"[执行者 {self.name}] 正在执行任务，产生结果...",
            AgentRole.CRITIC: f"[批评者 {self.name}] 正在审查，评估质量...",
            AgentRole.SUMMARIZER: f"[总结者 {self.name}] 正在汇总结果，生成报告...",
        }
        return responses.get(self.role, f"[{self.name}] 已处理请求。")
        
    def to_dict(self) -> Dict:
        """导出为字典"""
        return {
            "name": self.name,
            "role": self.role.value,
            "config": {
                "model": self.config.model,
                "temperature": self.config.temperature,
                "capabilities": self.config.capabilities,
            },
            "state": {
                "status": self.state["status"],
                "completed_tasks": len(self.state["completed_tasks"]),
            },
        }
        
    def __repr__(self) -> str:
        return f"<Agent {self.name} ({self.role.value})>"
