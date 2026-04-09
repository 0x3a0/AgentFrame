from abc import ABC, abstractmethod
from typing import Any, Optional

from openai import OpenAI


class BaseModel(ABC):
    """ BaseModel """

    @abstractmethod
    async def invoke(self,
        *,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, dict]]] = None,
    ):
        """ 调用模型 """
        pass

    @abstractmethod
    async def stream_invoke(self,
        *,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, dict]]] = None,
    ):
        """ 流式输出模型调用结果 """
        pass