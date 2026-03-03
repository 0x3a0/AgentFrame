from typing import Type
import pprint

from pydantic import BaseModel


class ToolRegistry:
    """ 
    ToolRegistry 类
    用于注册和管理工具实例
    该类提供了一个 register 装饰器方法，用于注册工具实例
    """
    def __init__(self):
        self.tools: list[dict[str, str]] = []

    def register(self, *, description: str, parameterModel: Type[BaseModel]):
        """ 
        注册 tool 的装饰器方法
        根据传入的参数模型生成符合 OpenAI 函数调用格式的 tool model
        :param description: 工具函数的描述
        :param parameterModel: 工具函数的参数模型
        """
        def wrapper(func):
            self.tools.append(
                {
                    "name": func.__name__,
                    "description": description,
                    "parameters": parameterModel.model_json_schema()
                }
            )

            return func

        return wrapper

    def print_tools(self):
        """ 列出当前已注册的工具 """
        for tool in self.tools:
            pprint.pprint(tool)