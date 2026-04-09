import os

import redis
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from loguru import logger

load_dotenv()
redis_url = os.getenv('REDIS_URL')
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv('API_KEY'),
    model_provider="openai",
    base_url=os.getenv('BASE_URL')
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ]
)

parser = StrOutputParser()


def get_session_history(session_id: str) -> RedisChatMessageHistory:
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=redis_url
        # ttl=3600  # 注释：关闭自动过期，避免重启后数据被清理
    )
    return history


history_chain = RunnableWithMessageHistory(
    chat_prompt | llm | parser,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

config = RunnableConfig(configurable={"session_id": "user-001"})

# 主循环
print("开始对话（输入 'quit' 退出）")
while True:
    question = input("\n输入问题：")
    if question.lower() in ['quit', 'exit', 'q']:
        break

    response = history_chain.invoke({"question": question}, config)
    logger.info(f"AI回答:{response}")

    # 等同于redis-cli的SAVE命令，强制写入dump.rdb
    redis_client.save()
