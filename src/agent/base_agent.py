from json import loads
from typing import Optional, Callable

from src.model import BaseModel


class BaseAgent:
    """ BaseAgent """
    def __init__(
        self,
        *,
        model: BaseModel,
        tools: Optional[list[Callable]] = None
    ):
        # 模型实例
        self.model = model

        # 工具
        if tools:
            self.tools = self._registry_tool(tools)


    def _registry_tool(self, tools: list[Callable]):
        """ 注册工具实例 """
        tool_descriptions = []
        for tool in tools:
            tool_descriptions.append(loads({
                "type": "function",
                "name": tool.__name__,
                "description": tool.__doc__.strip(),
                "parameters": {
                    "type": "object",
                    "properties": {
                        
                    }
                }
            }))
        print(tool_descriptions)

    def run(self):
        pass