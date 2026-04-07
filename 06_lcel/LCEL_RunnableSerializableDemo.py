import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

'''
串行链
RunnableSerializable-串行链
子链叠加串行，假如我们需要多次调用大模型，将多个步骤串联起来实现功能
'''
load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

#子链1提示词
chat_prompt_template1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个Ai专家，你的名字叫{name}"),
        ("human", "请问：{input}")
    ]
)
#子链1解释器
parser = StrOutputParser()
#子链1生成内容
chain1 = chat_prompt_template1 | llm | parser
response = chain1.invoke({"name": "小文", "input": "langchain是什么？要求简短，不超过50字"})
logger.info(f"chain1 response：{response}\n")

#子链2提示词
chat_prompt_template2 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个翻译专家，将用户输入的中文翻译成英文"),
        ("human", "{input}")
    ]
)
#子链2解释器
parser2 = StrOutputParser()
#子链2生成内容
chain2 = chat_prompt_template2 | llm | parser2

#串行链，将子链1返回的content作为子链2的input，执行子链2
# 组合成一个复合 Chain，使用 lambda 函数将chain1执行结果content内容添加input键作为参数传递给chain2
serializable_chain = chain1 | (lambda content: {"input": content}) | chain2
#串行链执行
final_response = serializable_chain.invoke({"name": "小文", "input": "langchain是什么？要求简短，不超过50字"})
logger.info(f"串行链返回内容：{final_response}")