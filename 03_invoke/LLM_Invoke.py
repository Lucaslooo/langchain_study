import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

#普通同步调用
#处理单条输入，等待LLM完全推理完成后再返回调用结果
load_dotenv()
llm = init_chat_model(
    model="qwen3.5-plus",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

messages = [
    SystemMessage("你是一个历史学家，可以回答历史知识，如果有其它不相关的问题，告知无法回复"),
    #HumanMessage("2+2=？")
    HumanMessage("清朝第一代皇帝是谁，帮我介绍一下，最多50字")
]
response = llm.invoke(messages)
print(f"响应类型：{type(response)}")
print(response.content)
