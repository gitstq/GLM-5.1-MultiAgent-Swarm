#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用例
"""

import pytest
import asyncio
from src.swarm import SwarmOrchestrator, Task, TaskStatus
from src.agent import Agent, AgentConfig, AgentRole
from src.message import Message, MessageType, MessageBus
from src.protocol import CommunicationProtocol, RequestResponseProtocol


class TestAgent:
    """Agent测试"""
    
    def test_create_agent(self):
        """测试创建Agent"""
        config = AgentConfig(name="TestAgent", role=AgentRole.EXECUTOR)
        agent = Agent(config)
        
        assert agent.name == "TestAgent"
        assert agent.role == AgentRole.EXECUTOR
        assert agent.state["status"] == "idle"
        
    def test_agent_update_state(self):
        """测试更新状态"""
        config = AgentConfig(name="TestAgent", role=AgentRole.EXECUTOR)
        agent = Agent(config)
        
        agent.update_state(status="working", current_task="test-task")
        
        assert agent.state["status"] == "working"
        assert agent.state["current_task"] == "test-task"
        
    def test_agent_add_message(self):
        """测试添加消息"""
        config = AgentConfig(name="TestAgent", role=AgentRole.EXECUTOR)
        agent = Agent(config)
        
        agent.add_message({"sender": "test", "content": "hello"})
        
        assert len(agent.state["messages"]) == 1
        assert agent.state["messages"][0]["content"] == "hello"
        
    def test_agent_to_dict(self):
        """测试导出字典"""
        config = AgentConfig(
            name="TestAgent",
            role=AgentRole.EXECUTOR,
            capabilities=["test"]
        )
        agent = Agent(config)
        
        result = agent.to_dict()
        
        assert result["name"] == "TestAgent"
        assert result["role"] == "executor"
        assert "test" in result["config"]["capabilities"]


class TestSwarmOrchestrator:
    """Swarm编排器测试"""
    
    def test_create_swarm(self):
        """测试创建Swarm"""
        swarm = SwarmOrchestrator(name="TestSwarm")
        
        assert swarm.name == "TestSwarm"
        assert len(swarm.agents) == 0
        assert len(swarm.tasks) == 0
        
    def test_create_agent(self):
        """测试创建Agent"""
        swarm = SwarmOrchestrator(name="TestSwarm")
        agent = swarm.create_agent("MyAgent", AgentRole.EXECUTOR)
        
        assert "MyAgent" in swarm.agents
        assert agent.role == AgentRole.EXECUTOR
        
    def test_create_default_team(self):
        """测试创建默认团队"""
        swarm = SwarmOrchestrator(name="TestSwarm")
        team = swarm.create_default_team()
        
        assert len(team) == 5
        assert len(swarm.agents) == 5
        
    def test_add_task(self):
        """测试添加任务"""
        swarm = SwarmOrchestrator(name="TestSwarm")
        task = swarm.add_task("Test task", task_id="test-1")
        
        assert "test-1" in swarm.tasks
        assert task.description == "Test task"
        assert task.status == TaskStatus.PENDING
        
    def test_assign_task(self):
        """测试分配任务"""
        swarm = SwarmOrchestrator(name="TestSwarm")
        swarm.create_default_team()
        task = swarm.add_task("Test task", task_id="test-1")
        
        result = swarm.assign_task("test-1", "TestSwarm-executor")
        
        assert result == True
        assert task.assigned_agent == "TestSwarm-executor"
        assert task.status == TaskStatus.IN_PROGRESS
        
    def test_get_status(self):
        """测试获取状态"""
        swarm = SwarmOrchestrator(name="TestSwarm")
        swarm.create_default_team()
        
        status = swarm.get_status()
        
        assert status["name"] == "TestSwarm"
        assert status["agents_count"] == 5


class TestMessage:
    """消息测试"""
    
    def test_create_message(self):
        """测试创建消息"""
        msg = Message(
            id="msg-1",
            msg_type=MessageType.TASK,
            sender="agent1",
            receivers=["agent2"],
            content="Test message"
        )
        
        assert msg.id == "msg-1"
        assert msg.msg_type == MessageType.TASK
        assert msg.content == "Test message"
        
    def test_message_to_dict(self):
        """测试消息转字典"""
        msg = Message(
            id="msg-1",
            msg_type=MessageType.RESULT,
            sender="agent1",
            receivers=["agent2"],
            content="Result"
        )
        
        result = msg.to_dict()
        
        assert result["id"] == "msg-1"
        assert result["type"] == "result"


class TestMessageBus:
    """消息总线测试"""
    
    def test_create_message_bus(self):
        """测试创建消息总线"""
        bus = MessageBus()
        
        assert len(bus.messages) == 0
        assert len(bus.subscriptions) == 0
        
    def test_send_message(self):
        """测试发送消息"""
        bus = MessageBus()
        msg = Message(
            id="msg-1",
            msg_type=MessageType.BROADCAST,
            sender="agent1",
            receivers=[],
            content="Hello"
        )
        
        result = bus.send(msg)
        
        assert result == True
        assert len(bus.messages) == 1
        
    def test_subscribe(self):
        """测试订阅"""
        bus = MessageBus()
        bus.subscribe("agent1", [MessageType.TASK])
        
        assert "agent1" in bus.subscriptions
        assert MessageType.TASK in bus.subscriptions["agent1"]


class TestProtocol:
    """协议测试"""
    
    def test_request_response_protocol(self):
        """测试请求响应协议"""
        protocol = RequestResponseProtocol(timeout=30)
        
        request = protocol.create_request(
            requester="agent1",
            target="agent2",
            action="execute",
            params={"task": "test"}
        )
        
        assert request["requester"] == "agent1"
        assert request["target"] == "agent2"
        assert request["action"] == "execute"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
