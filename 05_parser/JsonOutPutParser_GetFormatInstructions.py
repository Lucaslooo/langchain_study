import logging
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.adapters.openai import Chat
from langchain_core.output_parsers import JsonOutputParser, format_instructions
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
"""
JsonOutputParser，即JSON输出解析器，
是一种用于将大模型的自由文本输出转换为结构化JSON数据的工具。

本案例是：借助JsonOutputParser的get_format_instructions() ，
生成格式说明，指导模型输出JSON 结构
"""
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class Person(BaseModel):
    time:str = Field(description="时间"),
    person:str = Field(description="人物"),
    event:str = Field(description="事件")

# 创建JSON输出解析器，用于将model输出解析为Person对象
parser = JsonOutputParser(pydantic_object=Person)
# 获取格式化指令，告诉model如何输出符合要求的JSON格式
format_instruction = parser.get_format_instructions()

chat_prompt_template = ChatPromptTemplate(
    [
        ("system","你是一个AI助手，你只能输出结构化Json数据"),
        ("human","请生成一个关于{topic}的新闻。{format_instruction}")
    ]
)
# 格式化提示词，填入具体主题和格式化指令
prompt = chat_prompt_template.format_messages(
    topic="小米su7",
    format_instruction=format_instruction   #format_instruction = 给大模型看的「JSON 格式说明书」它会自动生成一段文字，告诉模型：必须返回什么样的 JSON、有哪些字段、每个字段是什么意思。
)
#格式化后的prompt
logger.info(prompt)

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

response = llm.invoke(prompt)
logger.info(f"模型原始输出: {response}\n")

final_response = parser.invoke(response)
logger.info(f"解析后的输出：: {final_response}\n")

logger.info(f"结果类型{type(final_response)}\n")