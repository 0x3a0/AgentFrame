from typing import Optional, Any

from .base_model import BaseModel

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk


class OpenAIChatModel(BaseModel):
    """ OpenAIChatModel """
    def __init__(
        self,
        *,
        model_name: str,
        openai_client: Optional[OpenAI] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.8,
        **kwargs: Any
    ):
        self.model_name = model_name
        if not openai_client:
            raise ValueError("OpenAIChatModel 中未提供 openai_client 实例")
        self.openai_client = openai_client

        # 系统提示词
        self.system_prompt = system_prompt or "你是一个AI助手, 你的名字是0xAI"
        
        # 对话参数
        self.temperature = temperature
        self.kwargs = kwargs

    def _build_messages(self, messages: list[dict[str, str]]) -> list[dict[str, str]]:
        """ 构建对话消息 """
        return [{"role": "system", "content": self.system_prompt}] + messages
   
    def stream_invoke(self,
        *,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, dict]]] = None
    ) -> Stream[ChatCompletionChunk]:
        """ 流式输出模型调用结果 """
        messages = self._build_messages(messages)
        resp = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tools,
            stream=True,
            temperature=self.temperature,
            **self.kwargs
        )
        for chunk in resp:
            yield chunk