import asyncio
from os import getenv
from dotenv import load_dotenv
from src.models import BaseModel


load_dotenv()

model = BaseModel(
    id="deepseek-chat",
    api_key=getenv("DEEPSEEK_API_KEY"),
    base_url=getenv("DEEPSEEK_BASE_URL"),
    extra_body={
        "thinking": {
            "type": "disabled"
        },
    },
    stream=True
)

resp = model.run([{"role": "user", "content": "你是谁？"}])
print(resp)