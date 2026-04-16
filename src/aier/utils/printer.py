from contextlib import contextmanager
from typing import Optional, Self
from textwrap import dedent

from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown


class Printer:
    _instance: Optional["Printer"] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.console = Console()

    @contextmanager
    def stream_print(self) -> None:
        """ 
            用于显示打印模型的流式响应, 该函数返回一个可调用的函数
            使用方法: 
                with printer.stream_print() as stream_print:
                    stream_print(resp.choices[0].delta.content)
        """
        text = Text()
        with Live(text) as live:
            def update(chunk_context: str):
                text.append(chunk_context)
                live.update(text)
            yield update

            text.append("\n")
            live.update(text)

    def user_content(self, message: str) -> None:
        self.console.print(f"[blue]>>[/blue] {message}\n")

    def assistant_content(self, message: str) -> None:
        pass

    def tool_info_content(
        self,
        function_name: str,
        function_args: dict
    ) -> None:
        self.console.print(f"[green]{function_name}[/green][dim]({function_args})[/dim]")

    def tool_result_content(self, result: str) -> None:
        self.console.print(result)
