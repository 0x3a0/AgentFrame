import asyncio
from os import getenv
from dotenv import load_dotenv
from src.models import ChatModel


load_dotenv()


async def main():
    model = ChatModel(
        model="glm-4.7-flash",
        api_key=getenv("GLM_API_KEY"),
        base_url=getenv("GLM_BASE_URL"),
    )
    async for chunk in model.dialog([{"role": "user", "content": "使用python完成一个快速排序算法"}]):
        print(chunk, end="")


if __name__ == "__main__":
    asyncio.run(main())