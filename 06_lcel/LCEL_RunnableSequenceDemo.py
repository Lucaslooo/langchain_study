import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

'''
RunnableSequence 顺序链调用  prompt | model | parser
LangChain 的一个典型链条由Prompt、Model、OutputParser （可没有）组成，
然后可以通过 链（Chain） 把它们顺序组合起来，让一个任务的输出成为下一个任务的输入
意思等价于Linux里面的管道符
'''

load_dotenv()

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个ai助手，名字叫{name}"),
        ("human", "请问：{input}")
    ]
)

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

parser = StrOutputParser()

# 构建处理链：提示词模板 | 模型 | 输出解析器
chain = chat_prompt_template | llm | parser

params = {
    "name": "小文",
    "input": "langchain是什么？用50字介绍一下"
}

#LCEL 链式调用传参 不能用 ** 展开，必须直接传字典,因为：**params 是 Python 函数关键字传参，chain.invoke(字典) 只接受一个参数（输入字典）
#response = chain.invoke(**params)
response = chain.invoke(params)

logger.info(f"lcel调用后的内容：{response}")
