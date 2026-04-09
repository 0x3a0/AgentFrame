from typing import Optional

from .base_model import BaseModel

from openai import OpenAI


class OpenAIChatModel(BaseModel):
    """ OpenAIChatModel """
    def __init__(
        self,
        *,
        model_name: str,
        openai_client: Optional[OpenAI] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.8,
        **kwargs
    ):
        self.model_name = model_name
        if not openai_client:
            raise ValueError("OpenAIChatModel 中未提供 openai_client 实例")
        self.openai_client = openai_client

        # 系统提示词
        self.system_prompt = "你是一个AI助手, 你的名字是0xAI"
        
        # 对话参数
        self.temperature = temperature
        self.kwargs = kwargs

    def invoke(self,
        *,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, dict]]] = None,
    ):
        """ 调用模型 """
        messages = [{"role": "system", "content": self.system_prompt}] + messages
        resp = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tools,
            temperature=self.temperature,
            **self.kwargs
        )
        return resp
   
    def stream_invoke(self,
        *,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, dict]]] = None,
    ):
        """ 流式输出模型调用结果 """
        pass