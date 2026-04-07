import logging
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个AI智能助手，你的名字是{name}。你的回答的结果返回json格式"),
        ("human","请回答：{input}")
    ]
)

prompt = chat_prompt_template.format_messages(
    name="小文",
    input="langchain是什么？要求简短，50字以内"
)

print(prompt)

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

base_response = llm.invoke(prompt)
logger.info(f"模型原始输出:{base_response}\n")
print("*" * 60)


#创建json输出解释器实例，只能把大模型输出的json格式的字符串转换为python字典，不能转换纯文字
parser = JsonOutputParser()
json_response = parser.invoke(base_response)
logger.info(f"解析后的输出：{json_response}\n")
logger.info(f"打印类型：{type(json_response)}")


