from typing import Any, Optional

from openai import OpenAI


class BaseModel:
    """ BaseModel """
    def __init__(
        self,
        id: str,
        api_key: str,
        base_url: str,
        temperature: float = 0.8,
        thinking: bool = False,
        stream: bool = False,
        timeout: float = 10,
        extra_body: Optional[Any] = None
    ):
        self.id = id
        self.api_key = api_key
        self.base_url = base_url

        # 对话参数
        self.temperature = temperature
        self.thinking = thinking
        self.stream = stream
        self.extra_body = extra_body

        # 是否打印对话记录
        self.show_messages = False

        # 客户端实例
        self.client: Optional[OpenAI] = None

        # 初始化客户端实例
        self._init_client()

    def _init_client(self) -> None:
        """ 初始化OpenAI客户端实例 """
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def _chat_completions(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: Optional[list] = None
    ) -> Any:
        """
        对话并获取原始响应

        Args:
            tools (Optional[list]): 工具列表, 默认 None.

        Return:
            OpenAIResponse: 模型响应.
        """
        resp = self.client.chat.completions.create(
            model=self.id,
            messages=messages,
            tools=tools,
            stream=self.stream,
            temperature=self.temperature,
            extra_body=self.extra_body
        )
        
        if self.stream:
            yield from resp
        else:
            return resp

    def invoke(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: Optional[list] = None
    ) -> Any:
        """
        通过调用 _chat_completions() 获取原始响应，并解析响应内容

        Args:
            tools (Optional[list]): 工具列表, 默认 None.

        Return:
            OpenAIResponse: 模型响应.
        """
        if self.stream:
            for chunk in self._chat_completions(messages, tools=tools):
                print(chunk)

    def get_client(self) -> Optional[OpenAI]:
        """ 返回一个OpenAI客户端实例 """
        if self.client:
            return self.client