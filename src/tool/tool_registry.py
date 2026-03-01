class Tool:
    """ 
    Tool 类
    用于注册和管理工具实例
    该类提供了一个 register 装饰器方法，用于注册工具实例
    """
    def __init__(self):
        self.tools = []

    def register(self, func):
        """ 提供注册工具的装饰器方法 """
        self.tools.append(
            {
                "name": func.__name__,
                "instruction": func.__doc__.strip(),
                "arguments": func.__annotations__
            }
        )
        return func

    def print_tools(self):
        print(self.tools)