from json import loads
from typing import Optional, Callable

from src.model import BaseModel
from src.tool import ToolRegistry
from src.memory import ShortTermMemory
from src.util import Printer


class BaseAgent:
    """ BaseAgent """
    def __init__(
        self,
        *,
        model: Optional[BaseModel] = None,
        system_prompt: Optional[str] = None,
        tools: Optional[ToolRegistry] = None
    ) -> None:
        # 模型实例
        if not model:
            raise ValueError("Agent 中未提供 model 实例")
        self.model = model

        # agent 系统提示
        # 初始化 agent 时，会将 agent 的 system prompt 覆盖 model 原先的 system prompt
        if system_prompt:
            model.system_prompt = system_prompt

        # 工具
        self.tools = tools

        # agent 短期记忆
        self.short_term_memory = ShortTermMemory()

        self.printer = Printer()

    def run(self, messages: dict[str, str]) -> None:
        """ 运行智能体 """
        tools = self.tools.get_registered_tools()
        tool_funcs = self.tools.get_registered_tool_funcs()

        self.printer.print_message(messages["content"], title=messages["role"])
        self.short_term_memory.add(messages)

        # agent loop
        while True:
            resp = self.model.invoke(self.short_term_memory.get_all_messages(), tools=tools)

            # 当不是 tool_calls 时，退出 agent loop
            if resp.choices[0].finish_reason != "tool_calls":
                llm_message_content = resp.choices[0].message.content
                self.short_term_memory.add({"role": "assistant", "content": llm_message_content})
                self.printer.print_message(llm_message_content, title="assistant")

                return llm_message_content

            else:
                # 处理工具调用
                tool_calls = resp.choices[0].message.tool_calls
                self.short_term_memory.add(
                    {
                        "role": "assistant",
                        "content": resp.choices[0].message.content,
                        "tool_calls": [
                            {
                                "id": tool_calls[0].id,
                                "type": "function",
                                "function": {
                                    "name": tool_calls[0].function.name,
                                    "arguments": tool_calls[0].function.arguments
                                }
                            }
                        ]
                    }
                )

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = loads(tool_call.function.arguments)

                    self.printer.print_message(
                        f"调用工具: {function_name}\nArguments: {function_args}",
                        title="using tool"
                    )

                    # 调用工具函数并获取结果
                    try:
                        result = tool_funcs[function_name](**function_args)
                    except Exception as e:
                        raise ValueError(f"工具 {function_name} 调用失败: {e}, 参数: {function_args}")
                    
                    self.printer.print_message(result, title="tool output")

                    self.short_term_memory.add({"role": "tool", "tool_call_id": tool_call.id, "content": result})


