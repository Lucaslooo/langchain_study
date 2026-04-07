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
"""
PydanticOutputParser 是 LangChain 输出解析器体系中最常用、最强大的结构化解析器之一。
它与 JsonOutputParser 类似，但功能更强 —— 能直接基于 Pydantic 模型 定义输出结构，
并利用其类型校验与自动文档能力。
对于结构更复杂、具有强类型约束的需求，PydanticOutputParser 则是最佳选择。
它结合了Pydantic模型的强大功能，提供了类型验证、数据转换等高级功能
"""


class Product(BaseModel):
    """
    产品信息模型类，用于定义产品的结构化数据格式

    属性:
        name (str): 产品名称
        category (str): 产品类别
        description (str): 产品简介，长度必须大于等于10个字符
    """
    name: str = Field(description="产品名称"),
    category: str = Field(description="产品描述")
    description: str = Field(description="产品简介")

    @field_validator("description")
    def validate_category(cls, value):
        """
        验证产品简介字段的长度
        参数:
            value (str): 待验证的产品简介文本
        返回:
            str: 验证通过的产品简介文本
        异常:
            ValueError: 当产品简介长度小于10个字符时抛出
        """
        if len(value) < 10:
            raise ValueError("产品简介的字数必须大于10")

        return value


# 创建Pydantic输出解析器实例，用于解析模型输出为Product对象
parser = PydanticOutputParser(pydantic_object=Product)
# 获取格式化指令，用于指导模型输出符合Product模型的JSON格式
format_instruction = parser.get_format_instructions()

chatgpt_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个Ai助手，你只能输出结构化的json数据\n{format_instruction}"), #简单结构 → format_instruction 放 human（强提醒);复杂结构 → 放 system（没问题）;想 100% 稳定 → 放 human（最保险）
        ("human", "请输出标题为{topic}的新闻内容")
    ]
)

# 格式化提示消息，填充主题和格式化指令
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
