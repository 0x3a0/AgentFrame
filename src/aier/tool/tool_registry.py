import inspect
from inspect import Parameter
from typing import Callable, Optional


class ToolRegistry:
    """ 
    ToolRegistry 类
    用于注册和管理工具实例
    该类提供了一个 register 装饰器方法，用于注册工具实例
    """
    def __init__(self) -> None:
        self.tools: list[Optional[dict[str, dict]]] = []
        self.tool_funcs: Optional[dict[str, Callable]] = {}

    def _load_defaults(self) -> None:
        """ 加载默认工具 """
        pass

    def _parse_arg_property(self, arg: Parameter) -> str:
        """ 解析参数类型 """
        arg_annotation = arg.annotation

        if arg_annotation is str:
            return {"type": "string"}

    def register(self, description: str) -> Callable:
        """ 
        注册 tool 的装饰器方法
        生成符合模型调用格式的 Function Tool
        
        :param description: 工具函数的描述
        """
        def wrapper(func):
            sig = inspect.signature(func)

            parameters = {
                "type": "function",
                "function": {
                    "name": func.__name__,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }

            # 提取参数信息
            for arg in sig.parameters.values():
                if arg.annotation is Parameter.empty:
                    raise TypeError(f"参数 '{arg.name}' 在工具函数 '{func.__name__}' 中缺少类型注解")

                arg_property = self._parse_arg_property(arg)
                parameters["function"]["parameters"]["properties"][arg.name] = arg_property
                parameters["function"]["parameters"]["required"].append(arg.name)
                # print(parameters)

            self.tools.append(parameters)
            self.tool_funcs[func.__name__] = func

            return func

        return wrapper

    def get_registered_tools(self):
        """ 获取已注册的工具列表 """
        return self.tools

    def get_registered_tool_funcs(self):
        """ 获取已注册的工具函数列表 """
        return self.tool_funcs