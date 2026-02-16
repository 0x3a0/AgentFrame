from src.cores import LLMClient


ACTOR_SYSTEM_PROMPT = """
你是一个资深的程序员，可以根据用户的需求，编写或完善代码。
你的代码必须包含必要的注释。
请直接输出代码，不需要输出任何额外的解释。
"""

EVALUATOR_SYSTEM_PROMPT = """
你是一位专业的代码评审专家和资深算法工程师，对代码的性能有着极致的要求。
你的任务是审查以下的代码，并找出代码的性能瓶颈，清晰地指出当前代码的不足之处，并提出具体的、可行的改进建议，但请不要输出优化代码。
当代码达到最优状态时，请直接输出"代码无需改进"。

请直接输出反馈，不要以MarkDown格式输出反馈。
"""


class Reflection:
    def __init__(self, llm_client: LLMClient, max_iterations: int = 5) -> None:
        self.llm_client = llm_client
        self.max_iterations = max_iterations
        self.actor_messages = [{"role": "system", "content": ACTOR_SYSTEM_PROMPT}]
        self.evaluator_messages = [{"role": "system", "content": EVALUATOR_SYSTEM_PROMPT}]

    def run(self, question: str) -> None:
        print(f"-------- ACTOR --------")
        print(f"Question: {question}")
        self.actor_messages.append({"role": "user", "content": question})

        # 生成初始答案
        first_answer = self.llm_client.generate(self.actor_messages)
        self.actor_messages.append({"role": "assistant", "content": first_answer})

        # 反思和优化
        print("-------- EVALUATOR --------")
        internal_feedback = ""
        self.evaluator_messages.append({"role": "user", "content": first_answer})
        for i in range(self.max_iterations):
            print(f"-------- 第{i + 1}轮 --------")
            # 模型反思以往的回答
            internal_feedback = self.llm_client.generate(self.evaluator_messages)
            if "代码无需改进" in internal_feedback:
                print("代码无需改进")
                break

            # 将评估结果添加到历史上下文中
            self.evaluator_messages.append({"role": "assistant", "content": internal_feedback})
            self.actor_messages.append({"role": "user", "content": internal_feedback})

            # 让模型根据评估结果优化原先的回答
            print("-------- ACTOR 优化回答 --------")
            refine_answer = self.llm_client.generate(self.actor_messages)
            self.actor_messages.append({"role": "assistant", "content": refine_answer})
            # 优化结果添加到Evaluator的历史上下文中
            self.evaluator_messages.append({"role": "user", "content": refine_answer})