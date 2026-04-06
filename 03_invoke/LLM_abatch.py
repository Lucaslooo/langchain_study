import asyncio
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

'''
异步批量调用
'''
#初始化大模型
load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

questions = [
    "你是谁？",
    "帮我解释一下为什么会下雨，要求简洁，不超过50字",
    "回答一下，跑步能减肥吗？要求简洁，不超过50字"
]


async def main():
    response = await llm.abatch(questions)  # abatch()批量处理异步请求
    print(f"响应类型：{type(response)}")  # 响应类型是list，所有要用await修饰
    for q, r in zip(questions, response):   # zip(questions, response)  把多个列表按照位置一一配对
        print(f"问题：{q}\n回答：{r.content}")


if __name__ == '__main__':
    asyncio.run(main())
