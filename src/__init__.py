#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-5.1-MultiAgent-Swarm
基于GLM-5.1的多智能体协作系统
Zero-dependency, 开箱即用

@author: gitstq
@license: MIT
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__email__ = "https://github.com/gitstq"
__license__ = "MIT"

from .agent import Agent, AgentRole
from .swarm import SwarmOrchestrator
from .message import Message, MessageType
from .protocol import CommunicationProtocol

__all__ = [
    "Agent",
    "AgentRole", 
    "SwarmOrchestrator",
    "Message",
    "MessageType",
    "CommunicationProtocol",
]
