import logging
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个Ai助手，你的名字是{name}"),
        ("human","请问：{input}")
    ]
)

prompt = chat_prompt_template.format_messages(
    name="小文",
    input="请介绍一下Python"
)

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

response = llm.invoke(prompt)
print(f"原始response: {response}\n")

parser = StrOutputParser()
final_response = parser.invoke(response)
print(f"解析后的response: {final_response}")