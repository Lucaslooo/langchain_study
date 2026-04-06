import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model="qwen3.5-plus",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

question = "你是谁"

response = llm.stream(question)
for chunk in response:
    print(chunk.content, end="")


