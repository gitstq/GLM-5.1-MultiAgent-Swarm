#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通信协议模块
定义Agent间的交互协议
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class ProtocolType(Enum):
    """协议类型"""
    REQUEST_RESPONSE = "request_response"  # 请求-响应模式
    PUB_SUB = "pub_sub"                    # 发布-订阅模式
    PIPELINE = "pipeline"                  # 管道模式


@dataclass
class ProtocolConfig:
    """协议配置"""
    name: str
    ptype: ProtocolType
    timeout: int = 30
    retries: int = 3
    validation: bool = True


class CommunicationProtocol:
    """通信协议基类"""
    
    def __init__(self, config: ProtocolConfig):
        self.config = config
        self.state: Dict[str, Any] = {}
        
    def validate_message(self, message: Dict) -> bool:
        """验证消息格式"""
        required_fields = ["type", "sender", "content"]
        if self.config.validation:
            return all(field in message for field in required_fields)
        return True
        
    def encode(self, message: Dict) -> str:
        """编码消息"""
        import json
        return json.dumps(message, ensure_ascii=False)
        
    def decode(self, data: str) -> Dict:
        """解码消息"""
        import json
        return json.loads(data)


class RequestResponseProtocol(CommunicationProtocol):
    """请求-响应协议"""
    
    def __init__(self, timeout: int = 30):
        super().__init__(ProtocolConfig(
            name="request_response",
            ptype=ProtocolType.REQUEST_RESPONSE,
            timeout=timeout,
        ))
        self.pending_requests: Dict[str, Any] = {}
        
    def create_request(
        self, 
        requester: str, 
        target: str, 
        action: str,
        params: Optional[Dict] = None
    ) -> Dict:
        """创建请求"""
        import uuid
        request_id = str(uuid.uuid4())[:8]
        
        request = {
            "type": "request",
            "request_id": request_id,
            "requester": requester,
            "target": target,
            "action": action,
            "params": params or {},
        }
        
        self.pending_requests[request_id] = {
            "status": "pending",
            "created_at": __import__("time").time(),
        }
        
        return request
        
    def create_response(
        self,
        request_id: str,
        target: str,
        status: str,
        result: Any = None,
        error: Optional[str] = None
    ) -> Dict:
        """创建响应"""
        return {
            "type": "response",
            "request_id": request_id,
            "target": target,
            "status": status,
            "result": result,
            "error": error,
        }


class PipelineProtocol(CommunicationProtocol):
    """管道协议 - 任务流水线"""
    
    def __init__(self):
        super().__init__(ProtocolConfig(
            name="pipeline",
            ptype=ProtocolType.PIPELINE,
        ))
        self.stages: List[str] = []
        
    def define_pipeline(self, stages: List[str]):
        """定义流水线阶段"""
        self.stages = stages
        
    def get_next_stage(self, current_stage: str) -> Optional[str]:
        """获取下一阶段"""
        try:
            idx = self.stages.index(current_stage)
            return self.stages[idx + 1] if idx + 1 < len(self.stages) else None
        except ValueError:
            return None
            
    def get_previous_stage(self, current_stage: str) -> Optional[str]:
        """获取上一阶段"""
        try:
            idx = self.stages.index(current_stage)
            return self.stages[idx - 1] if idx > 0 else None
        except ValueError:
            return None
