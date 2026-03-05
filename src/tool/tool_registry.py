from copy import deepcopy
from typing import Type, Callable

from pydantic import BaseModel


class ToolRegistry:
    """ 
    ToolRegistry 类
    用于注册和管理工具实例
    该类提供了一个 register 装饰器方法，用于注册工具实例
    """
    def __init__(self):
        self.tools: dict[str, dict] = {}

    def register(self, description: str, *, Model: Type[BaseModel]):
        """ 
        注册 tool 的装饰器方法
        根据传入的参数模型生成符合 OpenAI 函数调用格式的 tool model
        :param description: 工具函数的描述
        :param Model: 工具函数的参数模型
        """
        def wrapper(func):
            model_json_schema = Model.model_json_schema()
            # print(model_json_schema)
            args = model_json_schema["properties"].keys()
            for arg in args:
                self.tools[func.__name__] = {
                    "func": func,
                    "type": "function",
                    "function": {
                        "name": func.__name__,
                        "description": description,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                str(arg): {
                                    "type": model_json_schema["properties"][arg]["type"],
                                    "description": model_json_schema["properties"][arg]["description"]
                                }
                            },
                            "required": model_json_schema["required"]
                        }
                    }
                }
                
            return func

        return wrapper

    def get_registered_tools(self):
        """ 获取已注册的工具列表 """
        return self.tools
    
    def get_model_callable_tools(self):
        """ 获取模型可调用的工具列表 """
        tools = []
        for tool in deepcopy(self.tools).values():
            del tool['func']
            tools.append(tool)
        
        return tools