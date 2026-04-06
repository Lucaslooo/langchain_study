import asyncio
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

'''
普通异步调用：LangChain 提供 ainvoke() 异步调用接口，用于在 异步环境（async/await） 中高效并行地执行模型推理。
它的核心作用是：让你同时调用多个模型请求而不阻塞主线程 ------特别适合大批量请求或 Web 服务场景（如 FastAPI）
'''
#初始化大模型
load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


async def main():
    #异步调用一条请求
    response = await llm.ainvoke("解释一下langchain是什么，简洁回答100字以内")
    print(f"响应类型：{type(response)}")
    print(response.content_blocks)

#执行异步方法
if __name__ == "__main__":
    asyncio.run(main())
