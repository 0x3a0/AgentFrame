import logging
from typing import Optional


class Logger(object):
    _instance: Optional["Logger"] = None

    # 单例模式
    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        pass

    