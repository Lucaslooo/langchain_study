import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from loguru import logger

'''
"""
RunnableLambda-函数链
将普通Python函数融入Runnable流程.
"""
'''
load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

#子链1提示词
chat_prompt1 = ChatPromptTemplate(
    [
        ("system", "你是一个知识渊博的计算机专家"),
        ("human", "请用中文简短回答：{topic}是什么")
    ]
)
#子链1解释器
parser1 = StrOutputParser()
#子链1生成内容
chain1 = chat_prompt1 | llm | parser1


def debug_print(x):
    logger.info(f"中间结果：{x}")
    return {"input": x}


#子链2提示词
chat_prompt2 = ChatPromptTemplate(
    [
        ("system", "你是一个翻译专家，将用户输入内容翻译为英文"),
        ("human", "{input}")
    ]
)
#子链2解释器
parser2 = StrOutputParser()
#子链2生成内容
chain2 = chat_prompt2 | llm | parser2
# 创建一个可运行的调试节点，用于打印中间结果
debug_node = RunnableLambda(debug_print)

# 构建完整的处理链，将chain1、调试打印和chain2串联起来
full_chain = chain1 | debug_node | chain2

response = full_chain.invoke({"topic": "langchain是什么？要求简短，不超过50字"})
logger.info(f"full_chain_response = {response}")
