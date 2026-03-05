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
        extra_body: Optional[dict[str, Any]] = None,
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
        if extra_body is None:
            extra_body = {
                "thinking": {
                    "type": "disabled"
                }
            }
        self.extra_body = extra_body

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
            temperature=self.temperature,
            extra_body=self.extra_body
        )
        return resp
    
    def _merge_system_prompt_to_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """ 合并系统提示词和对话消息 """
        return [{"role": "system", "content": self.system_prompt}] + messages

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
        messages = self._merge_system_prompt_to_messages(messages)
        resp = self._chat_completions(messages, tools=tools)
        return resp

    def get_client(self) -> Optional[OpenAI]:
        """ 返回一个OpenAI客户端实例 """
        return self.client