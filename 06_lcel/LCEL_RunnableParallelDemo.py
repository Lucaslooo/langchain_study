import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from loguru import logger

'''
RunnableParallel-并行链

在 Langchain 中，创建并行链（Parallel Chains），是指同时运行多个子链（Chain），并在它们都完成后汇总结果。
**作用**：同时执行多个 Runnable，合并结果
'''
load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)
#并行链1提示词
chat_prompt1 = ChatPromptTemplate(
    [
        ("system", "你是一个知识渊博的计算机专家"),
        ("human", "请用中文简短回答：{topic}是什么")
    ]
)
#并行链1解释器
parser1 = StrOutputParser()
#并行链1生成内容
chain1 = chat_prompt1 | llm | parser1

#并行链2提示词
chat_prompt2 = ChatPromptTemplate(
    [
        ("system", "你是一个知识渊博的计算机专家"),
        ("human", "请用英文简短回答：{topic}是什么")
    ]
)
#并行链2解释器
parser2 = StrOutputParser()
#并行链2生成内容
chain2 = chat_prompt2 | llm | parser2

# 创建复合链,用于同时执行多个语言处理链
parallel_chain = RunnableParallel(
    {
        "chinese": chain1,  #运行 chain1，结果放进 "chinese"
        "english": chain2   #运行 chain2，结果放进 "english"
    }
)

# 调用复合链
response = parallel_chain.invoke({"topic": "langchain"})
logger.info(f"parallel_chain response:{response}")