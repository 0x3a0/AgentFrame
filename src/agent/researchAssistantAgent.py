import re
from json import loads, dumps

import requests
from openai import OpenAI
from dotenv import dotenv_values


CONFIG = dotenv_values(".env")

SYSTEM_PROMPT = """
你是一个专业的论文搜索助手，你的任务是根据用户的问题，并使用工具一步步解决问题，请严格遵守以下要求。

# 可用工具：
- 'search_paper_on_arxiv(keywords: str)': 在arXiv上搜索相关论文，返回一个包含论文信息的列表。

# 输出格式要求：
每次回复需严格遵守以下格式。

{
    "Thought": "思考过程和下一步计划",
    "Action": "执行的具体操作"
}

其中Action的格式必须是以下之一：
1. 调用工具时: 
{
    "function_name": "工具名称",
    "arguments": {
        "形参": "实参"
    }
}
2. 需要结束任务时: <finish>最终答案</finish>

# 重要提示：
- 每次只输出一个包含一对Thought和Action的JSON。
- 在调用工具前请将关键词翻译为英文。
- 当收集到足够的信息后，立马结束任务。
"""

ARXIV_SEARCH_API = "https://arxiv.org/api/query"


def search_paper_on_arxiv(keywords: str) -> list[dict]:
    """
    根据关键词在arXiv上搜索相关论文
    """
    resp = requests.get(
        url=ARXIV_SEARCH_API,
        params={
            "search_query": f"all:{keywords}",
            "start": 0,
            "max_results": 5
        }
    )
    # print(resp.text)
    papers = parse_arxiv_paper(resp.text)
    # print(papers)
    return papers

def parse_arxiv_paper(atom_content: str) -> list[dict]:
    """
    解析arXiv search API返回的Atom内容，提取论文信息
    """
    papers = []
    paper_atom_contents = atom_content.split("<entry>")[1:]
    for paper_atom_content in paper_atom_contents:
        paper_url = re.search(r"<id>(.*?)</id>", paper_atom_content)
        paper_title = re.search(r"<title>(.*?)</title>", paper_atom_content)
        paper_summary = re.search(r"<summary>(.*?)</summary>", paper_atom_content)
        papers.append({
            "url": paper_url.group(1),
            "title": paper_title.group(1),
            "summary": paper_summary.group(1)
        })

    return papers


class AgentClient:
    def __init__(self, model_id: str):
        self.client = OpenAI(
            api_key=CONFIG["API_KEY"],
            base_url=CONFIG["BASE_URL"]
        )
        self.model = model_id

    def get_complete(self, messages: list[dict]) -> str:
        """
        获取LLM的回复
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8
        )
        return resp.choices[0].message.content


# 可用工具
tools = {
    "search_paper_on_arxiv": search_paper_on_arxiv
}

def main() -> None:
    agent_client = AgentClient(model_id="deepseek-ai/DeepSeek-V3.2")
    user_prompt = "我现在需要完成一篇关于多智能体的论文，但没有思路，你可以帮我搜索一些相关的论文并简单的总结一下吗？"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    # 智能体主循环
    for i in range(10):
        print(f"--------------- 第{i + 1}轮对话 -----------------\n")
        llm_output = agent_client.get_complete(messages=messages)
        print(f"模型输出: {llm_output}\n")

        messages.append({
            "role": "assistant",
            "content": llm_output
        })
        if "<finish>" in llm_output:
            print("任务完成")
            break
        
        # 调用工具
        if "function_name" in llm_output:
            action_json = loads(llm_output)
            function_name = action_json["Action"]["function_name"]
            arguments = action_json["Action"]["arguments"]
            # 获取论文信息
            papers = tools[function_name](**arguments)
            print(f"获取到的论文信息: {papers}\n")
            messages.append({
                "role": "user",
                "content": f"Observation: [工具调用结果] {papers}"
            })


if __name__ == "__main__":
    main()