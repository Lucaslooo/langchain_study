import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

chat_prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个数学工程师，你的名字是{name}"),
        ("human", "你能帮我做什么？"),
        ("ai", "我能帮你解答{type}问题"),
        ("human", "好的，那{user_input}")  #模型只会回答最后一句human问题。前面的都是作为历史上下文
    ]
)

prompt = chat_prompt_template.format_messages(
    name="小问AI", type="数学", user_input="请问二元一次方程组该怎么解，要求简短"
)
print(prompt)

load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)
response = llm.invoke(prompt)
print(response)
print(response.content)
