from ast import literal_eval
from src.cores import LLMClient


SOLVER_PROMPT_TEMPLATE = """
你是一个善于执行计划的专家，你的任务是严格按照给定的计划一步步完成任务。
你会收到原始问题、完整的计划列表、目前已完成的任务结果，以及当前需要完成的任务。
请专注于当前需要完成的任务，回答时仅输出当前任务的结果。

# 原始问题
{question}

# 计划列表
{plans}

# 已完成的任务结果
{completed_tasks}

# 当前要完成的任务
{current_tasks}
"""

PLANNER_SYSTEM_PROMPT = """
你是一个规划专家，你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的计划表。
请确保计划中的每一步骤都是独立、可执行的子任务，严格按照逻辑顺序排序。
输出的计划必须是一个python列表，列表内的每一个元素都是一个描述子任务的字符串。

请严格按照以下格式输出你的行动计划：
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""


class Planner:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.messages = [{"role": "system", "content": PLANNER_SYSTEM_PROMPT}]

    def _add_message(self, role: str, message: str) -> None:
        """
        添加对话消息
        :param role: 角色
        :param message: 内容
        """
        self.messages.append({"role": role, "content": message})

    def plan(self, question: str) -> list[str]:
        """
        规划计划
        :param question: 用户问题
        """
        print("---------- Planner ----------")
        print(f"question: {question}")

        self._add_message("user", question)
        llm_output = self.llm_client.generate(self.messages)
        self._add_message("assistant", llm_output)

        plans = llm_output.split("```python")[1].split("```")[0].strip()
        print(f"plans: {plans}")
        return literal_eval(plans)


class Solver:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client
        self.completed_tasks = ""

    def solve(self, question: str, plans: list[str]) -> None:
        """
        解决计划
        :param question: 用户问题
        :param plans: 计划列表
        :param completed_tasks: 已完成的任务和结果
        :param current_tasks: 当前需要执行的任务
        :return: 解决结果
        """
        print("---------- Solver ----------")
        for step, plan in enumerate(plans):
            messages = [{
                "role": "user",
                "content": SOLVER_PROMPT_TEMPLATE.format(
                    question=question,
                    plans=plans,
                    completed_tasks=self.completed_tasks,
                    current_tasks=plan
                )
            }]

            llm_output = self.llm_client.generate(messages)

            # 添加已完成的任务结果
            self.completed_tasks += f"{step + 1}. {llm_output.strip()}\n"
            print(f"步骤{step + 1}/{len(plans)}：\"{plan}\"，运行结果：\"{llm_output}\"\n")
