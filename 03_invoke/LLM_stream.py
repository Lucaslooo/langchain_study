'''
普通流式调用：
'''
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

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
    HumanMessage(content="你是谁？今天上海天气怎么样？")
]

response = llm.stream(messages)
print(f"响应类型{type(response)}")
'''
响应类型为generator：一边循环、一边计算、一边往外吐数据的 “懒家伙”
特点：1、懒加载（不占内存）；2、只能迭代一次，不能回头；3、必须用for循环/next（）才能取出数据
'''
for chunk in response:
    print(chunk.content, end="")
