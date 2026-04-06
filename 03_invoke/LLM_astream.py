import asyncio
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
'''
异步流式调用：
'''
#初始化大模型
load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

messages = [
    SystemMessage(content="你是小文，是一个热心的AI人工助手"),
    HumanMessage(content="你是谁？")
]


async def main():
    response = llm.astream(messages)  # astream()返回的不是结果，而是异步生成器(async generator),异步生成器不能await，只能用async for遍历
    print(f"响应类型：{type(response)}")
    async for chunk in response:
        #刷新缓冲区，实现流式输出
        print(chunk.content, end="", flush=True)


print("\n")

if __name__ == "__main__":
    asyncio.run(main())
