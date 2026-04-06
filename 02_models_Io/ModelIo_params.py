import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    #temperature=0.0 温度越高，输出内容越随机；温度越低，输出内容越确定
    temperature=0.8
)

question = "帮我写一句关于描述春天的诗，要求十四字以内"

for x in range(3):
    print(llm.invoke(question).content+"\n")
