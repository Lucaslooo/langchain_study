# 设置本地模型
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from loguru import logger

load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url=os.getenv("BASE_URL")
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human","{input}")
    ]
)
parser = StrOutputParser()

chain = chat_prompt | llm | parser
#创建存历史记录的盒子
history = InMemoryChatMessageHistory()

runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=(lambda session_id:history),
    input_messages_key="input",
    history_messages_key="history"
)

config = RunnableConfig(configurable={"session_id": "user-001"})

logger.info(runnable.invoke({"input": "我叫张三，我爱好学习。"}, config))
logger.info(runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config))
