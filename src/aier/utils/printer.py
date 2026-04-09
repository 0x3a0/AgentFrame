from typing import Optional, Self

from rich import print as rich_print
from rich.panel import Panel


class Printer:
    _instance: Optional["Printer"] = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        pass

    def print_message(self, message: str, *, title: str) -> None:
        rich_print(Panel(
            message,
            title=title,
            title_align="left",
            padding=(1, 2)
        ))
        rich_print()