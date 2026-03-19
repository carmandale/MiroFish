"""
LLM客户端封装
统一使用OpenAI格式调用
"""

import json
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config


class LLMClient:
    """LLM客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY 未配置")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    @staticmethod
    def model_uses_max_completion_tokens(model_name: Optional[str]) -> bool:
        """GPT-5 系列在 Chat Completions 中使用 `max_completion_tokens`。"""
        return (model_name or "").lower().startswith("gpt-5")

    @classmethod
    def compatibility_kwargs(
        cls,
        model_name: Optional[str],
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        生成兼容不同模型家族的请求参数。

        GPT-5 系列：
        - `max_completion_tokens` 替代 `max_tokens`
        - 仅支持默认 temperature，因此非 1 的值直接省略，让服务端使用默认值
        """
        kwargs: Dict[str, Any] = {}
        if max_tokens is not None:
            if cls.model_uses_max_completion_tokens(model_name):
                kwargs["max_completion_tokens"] = max_tokens
            else:
                kwargs["max_tokens"] = max_tokens

        if temperature is not None:
            if cls.model_uses_max_completion_tokens(model_name):
                if temperature == 1:
                    kwargs["temperature"] = temperature
            else:
                kwargs["temperature"] = temperature

        return kwargs

    def _token_limit_kwargs(self, max_tokens: int) -> Dict[str, int]:
        """
        兼容不同 OpenAI 兼容模型的 token 限制参数名。

        GPT-5 系列在 Chat Completions 中要求 `max_completion_tokens`，
        其余现有调用继续使用 `max_tokens`。
        """
        compatibility = self.compatibility_kwargs(self.model, max_tokens=max_tokens)
        return {
            key: value
            for key, value in compatibility.items()
            if key in {"max_tokens", "max_completion_tokens"}
        }
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式（如JSON模式）
            
        Returns:
            模型响应文本
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            **self._token_limit_kwargs(max_tokens),
            **{
                key: value
                for key, value in self.compatibility_kwargs(self.model, temperature=temperature).items()
                if key == "temperature"
            },
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        # 部分模型（如MiniMax M2.5）会在content中包含<think>思考内容，需要移除
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
        return content
    
    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        发送聊天请求并返回JSON
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            解析后的JSON对象
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        # 清理markdown代码块标记
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^```(?:json)?\s*\n?', '', cleaned_response, flags=re.IGNORECASE)
        cleaned_response = re.sub(r'\n?```\s*$', '', cleaned_response)
        cleaned_response = cleaned_response.strip()

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            raise ValueError(f"LLM返回的JSON格式无效: {cleaned_response}")
