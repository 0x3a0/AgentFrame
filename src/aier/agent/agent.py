from json import loads
from typing import Optional, Callable, Any

from aier.model import BaseModel
from aier.tool import ToolRegistry
from aier.memory import ShortTermMemory
from aier.utils import Printer


class Agent:
    """ Agent """
    def __init__(
        self,
        *,
        model: BaseModel,
        system_prompt: Optional[str] = None,
        tools: Optional[ToolRegistry] = None
    ) -> None:
        self.model = model

        # 在初始化 agent 时，会将 agent 的 system prompt 覆盖 model 原先的 system prompt
        if system_prompt:
            model.system_prompt = system_prompt

        # 工具
        self.tools = tools

        # agent 短期记忆
        self.short_term_memory = ShortTermMemory()

        self.printer = Printer()

    def _execute_tool_call(self, tool_call_buffer: dict) -> Any:
        """ 执行工具调用 """
        tool_funcs = self.tools.get_registered_tool_funcs()
        
        # 执行工具
        function_name = tool_call_buffer["name"]
        function_args = loads(tool_call_buffer["arguments"])
        
        # 执行工具
        try:
            self.printer.tool_info_content(function_name, function_args)
            result = tool_funcs[function_name](**function_args)
            self.printer.tool_result_content(f"[green]√[/green] [dim]{result}[/dim]\n")
        except Exception as e:
            raise ValueError(f"工具 {function_name} 调用失败: {e}, 参数: {function_args}")
        
        return result

    def run(self, input: str) -> None:
        """ 运行智能体 """
        self.short_term_memory.add({"role": "user", "content": input})
        self.printer.user_content(input)

        # agent loop
        while True:
            content_buffer = ""
            tool_call_buffer = {}
            
            with self.printer.stream_print() as stream_print:
                for chunk in self.model.stream_invoke(
                    messages=self.short_term_memory.all_messages(),
                    tools=self.tools.get_registered_tools()
                ):
                    # print(chunk)
                    delta = chunk.choices[0].delta
                    
                    # 处理文本内容
                    if delta.content:
                        content_buffer += delta.content
                        stream_print(delta.content)
                    
                    # 处理工具调用
                    if delta.tool_calls:
                        for tool_call in delta.tool_calls:
                            if tool_call.id:
                                tool_call_buffer = {
                                    "id": tool_call.id,
                                    "name": "",
                                    "arguments": ""
                                }

                            if tool_call.function.name:
                                tool_call_buffer["name"] = tool_call.function.name
                            if tool_call.function.arguments:
                                tool_call_buffer["arguments"] += tool_call.function.arguments
                    
            # 检查是否有工具调用
            if tool_call_buffer:
                # 添加到记忆
                self.short_term_memory.add({
                    "role": "assistant",
                    "content": content_buffer,
                    "tool_calls": [
                        {
                            "id": tool_call_buffer["id"],
                            "type": "function",
                            "function": {
                                "name": tool_call_buffer["name"],
                                "arguments": tool_call_buffer["arguments"]
                            }
                        }
                    ]
                })

                # 执行工具调用获取结果
                result = self._execute_tool_call(tool_call_buffer)

                # 添加工具结果到记忆
                self.short_term_memory.add({
                    "role": "tool",
                    "tool_call_id": tool_call_buffer["id"],
                    "content": str(result)
                })

                continue
            else:
                self.short_term_memory.add({"role": "assistant", "content": content_buffer})
                break