from os import getenv
from dotenv import load_dotenv

from aier.model import OpenAI, OpenAIChatModel
from aier.agent import Agent
from aier.tool import ToolRegistry


load_dotenv()

client = OpenAI(api_key=getenv("DEEPSEEK_API_KEY"), base_url=getenv("DEEPSEEK_BASE_URL"))
model = OpenAIChatModel(
    model_name="deepseek-chat",
    openai_client=client
)

tools = ToolRegistry()

@tools.register(
    description="获取城市天气",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "需要查询的城市名称"
            }
        },
        "required": ["city"]
    }
)
def get_weather(city: str) -> str:
    return f"{city}的天气是晴天，当前气温25℃"

@tools.register(
    description="获取用户当前所在的位置",
    parameters={
        "type": "object",
        "properties": {},
        "required": []
    }
)
def get_location() -> str:
    return "天津"

agent = Agent(
    model=model,
    tools=tools
)

resp = agent.run("我要出门了，帮我看看今天的天气如何")