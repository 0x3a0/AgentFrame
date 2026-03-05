from typing import Optional, Callable

from src.model import BaseModel


class BaseAgent:
    """ BaseAgent """
    def __init__(
        self,
        *,
        model: BaseModel,
        system_prompt: Optional[str] = None,
        tools: Optional[list[Callable]] = None
    ):
        # 模型实例
        self.model = model

        # 系统提示
        if system_prompt:
            model.system_prompt = system_prompt

        # 工具
        self.tools = tools

    def run(self, messages: list[dict[str, str]]):
        """ 运行智能体 """
        model_tools = self.tools.get_model_callable_tools()
        resp = self.model.invoke(messages, tools=model_tools)
        return resp