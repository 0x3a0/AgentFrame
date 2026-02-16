from  typing import Any, Optional
from os import getenv
from openai import OpenAI


class ChatModel:
    """Model"""
    def __init__(
        self,
        id: str,
        api_key: str,
        base_url: str,
        temperature: float = 1.0,
        thinking: bool = False,
        stream: bool = False
    ):
        self.id = id
        self.api_key = api_key
        self.base_url = base_url

        # 对话参数
        self.temperature = temperature
        self.thinking = thinking
        self.stream = stream

        self.client: Optional[OpenAI] = None

    def get_client(self) -> Optional[OpenAI]:
        """ 返回一个OpenAI客户端实例 """
        if self.client:
            pass

    def invoke(
        self,
        messages: list[dict[str, Any]]
    ) -> None:
        """
        通过 OpenAI API 与模型对话并获取响应

        Args:
            messages (list[dict[str, Any]]): 需要发送给模型的历史对话列表
        """
        pass