"""
GLM-5.1 MultiAgent Swarm
基于GLM-5.1的多智能体协作系统

一个轻量级、高效的多Agent协作框架，
支持任务分解、并行执行、层级协作。

@author: gitstq
@license: MIT
"""

from src.swarm import SwarmOrchestrator, Task, TaskStatus
from src.agent import Agent, AgentRole, AgentConfig
from src.message import Message, MessageType, MessageBus
from src.protocol import CommunicationProtocol, RequestResponseProtocol
from src.client import GLMClient, async_chat

__version__ = "1.0.0"
__all__ = [
    "SwarmOrchestrator",
    "Task",
    "TaskStatus",
    "Agent",
    "AgentRole",
    "AgentConfig",
    "Message",
    "MessageType",
    "MessageBus",
    "CommunicationProtocol",
    "RequestResponseProtocol",
    "GLMClient",
    "async_chat",
]
