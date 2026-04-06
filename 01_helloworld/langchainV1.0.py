import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
model = init_chat_model(
    model=os.getenv("QWEN_MODEL"),
    model_provider="openai",
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

print(model.invoke("你是谁").content)
