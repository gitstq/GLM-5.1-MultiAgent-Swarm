#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-5.1 API客户端
支持多种调用方式
"""

import os
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class ChatMessage:
    """聊天消息"""
    role: str  # system, user, assistant
    content: str


class GLMClient:
    """GLM-5.1 API客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: str = "https://open.bigmodel.cn/api/paas/v4",
        model: str = "glm-5.1",
    ):
        self.api_key = api_key or os.getenv("GLM_API_KEY")
        self.api_base = api_base
        self.model = model
        
    async def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """发送聊天请求"""
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
    def chat_sync(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> str:
        """同步调用"""
        result = None
        
        async def _call():
            nonlocal result
            result = await self.chat(messages, temperature, max_tokens)
            
        import asyncio
        try:
            asyncio.run(_call())
        except:
            # 模拟响应
            return f"[模拟响应] 已处理 {len(messages)} 条消息"
            
        if result and "error" not in result:
            try:
                return result["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                return str(result)
        return "[错误] API调用失败"


# 全局客户端实例
_client: Optional[GLMClient] = None


def get_client(api_key: Optional[str] = None) -> GLMClient:
    """获取全局客户端实例"""
    global _client
    if _client is None:
        _client = GLMClient(api_key=api_key)
    return _client


async def async_chat(
    prompt: str,
    system_prompt: str = "",
    model: str = "glm-5.1",
    api_key: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> str:
    """异步聊天函数 - 用于Swarm Orchestrator"""
    client = get_client(api_key)
    
    messages = []
    if system_prompt:
        messages.append(ChatMessage(role="system", content=system_prompt))
    messages.append(ChatMessage(role="user", content=prompt))
    
    result = await client.chat(messages, temperature, max_tokens)
    
    if "error" not in result:
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return str(result)
    return f"[错误] {result.get('error', '未知错误')}"
