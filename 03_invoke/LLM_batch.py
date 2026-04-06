import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

'''
普通批量调用：
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

response = llm.batch(questions)
print(f"响应类型：{type(response)}")

for q, r in zip(questions, response):
    print(f"问题：{q}\n回答：{r.content}\n")

