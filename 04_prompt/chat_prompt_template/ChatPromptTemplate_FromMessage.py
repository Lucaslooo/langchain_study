import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}，你的职责是{job},请回答我的问题"),
        ("human", "请回答，{question}")
    ]
)
params = {
    "role": "AI开发工程师",
    "job": "解答ai相关的问题",
    "question": "langchain是什么？"
}
chat_prompt = chat_prompt_template.format_messages(
    **params)  #**params 解包

load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

response = llm.invoke(chat_prompt)
print(response.content)
