from os import getenv
from dotenv import load_dotenv

from aier.model import BaseModel
from aier.agent import BaseAgent
from aier.tool import ToolRegistry


load_dotenv()

model = BaseModel(
    id="deepseek-chat",
    api_key=getenv("DEEPSEEK_API_KEY"),
    base_url=getenv("DEEPSEEK_BASE_URL")
)

tools = ToolRegistry()

@tools.register("获取城市天气")
def get_weather(city: str) -> str:
    return f"{city}的天气是晴天，当前气温25℃"

agent = BaseAgent(
    model=model,
    system_prompt="你是一个旅行助手，你的名字为0x01",
    tools=tools
)

resp = agent.run({"role": "user", "content": "帮我查询广西南宁今天的天气"})