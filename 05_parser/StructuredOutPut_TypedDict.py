import logging
import os
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

class Animal(TypedDict):
    animal: Annotated[str,"动物"]
    emoji: Annotated[str,"表情"]

class AnimalList(TypedDict):
    animals: Annotated[list[Animal],"动物列表"]


chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("human","{input}")
    ]
)

prompt = chat_prompt_template.format_messages(input="请生成3种动物，以及他们的emoji表情，返回json结果")

llm_structured = llm.with_structured_output(AnimalList)
response = llm_structured.invoke(prompt)
print(response)
