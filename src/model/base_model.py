from typing import Any, Optional

from openai import OpenAI


class BaseModel:
    """ BaseModel """
    def __init__(
        self,
        *,
        id: str,
        api_key: str,
        base_url: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.8,
        thinking: bool = False,
        stream: bool = False,
        extra_body: Optional[dict[str, Any]] = None,
        show_messages: bool = False
    ):
        # 客户端参数
        self.id = id
        self.api_key = api_key
        self.base_url = base_url

        # 系统提示词
        if system_prompt is None:
            system_prompt = "你是一个AI助手"
        self.system_prompt = system_prompt
        
        # 对话参数
        self.temperature = temperature
        self.thinking = thinking
        self.stream = stream
        if extra_body is None:
            extra_body = {
                "thinking": {
                    "type": "disabled"
                }
            }
        self.extra_body = extra_body

        # 是否打印对话记录。当为 True 时，用户和模型的每一次对话都会打印到控制台当中
        self.show_messages = show_messages

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
            messages (list[dict[str, Any]]): 对话消息列表.
            tools (Optional[list]): 工具列表, 默认 None.

        Return:
            
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

    def show_message(self):
        pass

    def invoke(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: Optional[list] = None
    ) -> Any:
        """
        通过调用 _chat_completions() 获取原始响应，并解析响应内容

        Args:
            messages (list[dict[str, Any]]): 对话消息列表.
            tools (Optional[list]): 工具列表, 默认 None.

        Return:
            
        """
        if self.show_messages:
            for char in messages[-1]["role"] + ": " + messages[-1]["content"]:
                print(char, end="", flush=True)
            
            print("\n")

        if self.stream:
            message = ""

            if self.show_messages:
                for char in "assistant: ":
                    print(char, end="", flush=True)

            for chunk in self._chat_completions(messages, tools=tools):
                chunk_content = chunk.choices[0].delta.content
                message += chunk_content

                if self.show_messages:
                    print(chunk_content, end="", flush=True)
                
            print("\n")

        else:
            resp = self._chat_completions(messages, tools=tools)
            print(resp)

    def get_client(self) -> Optional[OpenAI]:
        """ 返回一个OpenAI客户端实例 """
        if self.client:
            return self.client