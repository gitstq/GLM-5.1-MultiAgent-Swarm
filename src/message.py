#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息传递模块
支持Agent间的异步通信
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from datetime import datetime


class MessageType(Enum):
    """消息类型"""
    TASK = "task"                   # 任务消息
    RESULT = "result"               # 结果消息
    QUERY = "query"                 # 查询消息
    RESPONSE = "response"           # 响应消息
    NOTIFICATION = "notification"   # 通知消息
    REQUEST = "request"             # 请求消息
    BROADCAST = "broadcast"         # 广播消息


class Priority(Enum):
    """消息优先级"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Message:
    """消息类"""
    id: str
    msg_type: MessageType
    sender: str
    receivers: list  # 空列表表示广播
    content: Any
    priority: Priority = Priority.NORMAL
    metadata: Dict = field(default_factory=dict)
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    reply_to: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.msg_type.value,
            "sender": self.sender,
            "receivers": self.receivers,
            "content": str(self.content)[:200],
            "priority": self.priority.name,
            "created_at": self.created_at,
            "reply_to": self.reply_to,
        }
    
    def __str__(self) -> str:
        return f"[{self.msg_type.value}] {self.sender} -> {self.receivers or 'BROADCAST'}: {str(self.content)[:50]}..."


class MessageBus:
    """消息总线 - 支持Agent间通信"""
    
    def __init__(self):
        self.messages: list = []
        self.subscriptions: Dict[str, list] = {}  # agent -> message_types
        
    def send(self, message: Message) -> bool:
        """发送消息"""
        self.messages.append(message)
        print(f"[MessageBus] 消息发送: {message}")
        return True
    
    def subscribe(self, agent_name: str, msg_types: list = None):
        """订阅消息"""
        if agent_name not in self.subscriptions:
            self.subscriptions[agent_name] = []
        if msg_types:
            self.subscriptions[agent_name].extend(msg_types)
            
    def get_messages(self, agent_name: str, msg_type: MessageType = None) -> list:
        """获取消息"""
        received = []
        for msg in self.messages:
            # 检查是否是接收者或是广播
            if (agent_name in msg.receivers or not msg.receivers):
                if msg_type is None or msg.msg_type == msg_type:
                    received.append(msg)
        return received
    
    def broadcast(self, sender: str, content: Any, priority: Priority = Priority.NORMAL) -> Message:
        """广播消息"""
        msg = Message(
            id=f"msg-{len(self.messages) + 1}",
            msg_type=MessageType.BROADCAST,
            sender=sender,
            receivers=[],
            content=content,
            priority=priority,
        )
        return self.send(msg)
