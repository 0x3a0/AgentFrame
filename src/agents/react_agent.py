from json import loads
from src.cores.base_agent import BaseAgent
from src.utils import tools


SYSTEM_PROMPT = """
你是一个金融智能助手，你的任务是回答用户的问题。

# 可用工具
- search_fund(fund_id: str): 搜索基金信息

# 输出格式
每次输出请严格按照以下格式：
{
    "Thought": [思考过程，用于分析问题、拆解复杂任务和规划下一步行动]
    "Action": [采取的行动]
}
- 其中，Action字段的格式必须为以下之一：
    1. 调用工具: 
    {
        "function_name": "工具名称",
        "arguments": {
            "形参": "实参"
        }
    }
    2. 输出最终答案(当收集到足够多的信息，能回答用户问题时，必须在Action字段后输出最终答案，输出的答案不要跨行): <finish>最终答案</finish>
"""


class ReAct:
    def __init__(self, llm_client: LLMClient, max_steps: int = 10) -> None:
        self.llm_client = llm_client
        self.max_steps = max_steps

        # 对话上下文
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _add_message(self, role: str, content: str) -> None:
        """
        添加对话消息
        :param role: 角色
        :param content: 内容
        """
        self.messages.append({"role": role, "content": content})
    
    def run(self, question: str) -> str:
        """
        运行ReActAgent
        :param question: 用户问题
        :return: 返回最终答案
        """
        self._add_message("user", question)
        for step in range(self.max_steps):
            print(f"-------- 第{step + 1}轮对话 --------")
            llm_output = self.llm_client.generate(self.messages)
            self._add_message("assistant", llm_output)

            llm_output_json = loads(llm_output)
            if "<finish>" in llm_output_json["Action"]:
                print("任务完成")
                break

            # 调用工具
            if "function_name" in llm_output_json["Action"]:
                function_name = llm_output_json["Action"]["function_name"]
                arguments = llm_output_json["Action"]["arguments"]
                # 获取工具信息
                result = tools[function_name](**arguments)
                self._add_message("user", f"Observation[工具调用结果]: {result}")

