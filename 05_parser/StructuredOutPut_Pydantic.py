import logging
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, field_validator
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Product(BaseModel):
    name : str = Field(description="产品名称"),
    category: str = Field(description="产品描述")
    description: str = Field(description="产品简介")

    @field_validator("description")
    def validate_category(cls,value):
        if len(value) < 10:
            raise ValueError("产品简介的字数必须大于10")

        return value

parser = PydanticOutputParser(pydantic_object=Product)
format_instruction = parser.get_format_instructions()

chatgpt_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个Ai助手，你只能输出结构化的json数据\n{format_instruction}"),
        ("human","请输出标题为{topic}的新闻内容")
    ]
)

prompt = chatgpt_prompt_template.format_messages(
    format_instruction=format_instruction,
    topic="华为手机"
)
#格式化后的提示词
logger.info(prompt)

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

response = llm.invoke(prompt)
logger.info(f"原始response: {response}")

parser_response = parser.invoke(response)
logger.info(f"格式化后的response：: {parser_response}")