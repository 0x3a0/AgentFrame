from json import loads
from typing import Optional, Callable

from src.model import BaseModel


class BaseAgent:
    """ BaseAgent """
    def __init__(
        self,
        *,
        model: BaseModel,
        system_prompt: Optional[str] = None,
        tool: Optional[list[Callable]] = None
    ):
        # 模型实例
        self.model = model

        # 系统提示
        if system_prompt:
            model.system_prompt = system_prompt
            self.system_prompt = system_prompt
        else:
            self.system_prompt = model.system_prompt

        # 工具
        self.tools = tools

    def run(self):
        pass