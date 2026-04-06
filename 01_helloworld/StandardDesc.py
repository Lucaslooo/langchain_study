import logging
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.exceptions import LangChainException
from langchain_core.language_models import BaseChatModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()


def init_llm_client() -> BaseChatModel:
    #1、从配置文件获取api_key，做空值校验
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("环境变量API_KEY未配置，请检查配置文件")

    #2、初始化LLM客户端，采用v1.0的方式
    llm = init_chat_model(
        model="qwen3.5-plus",
        api_key=api_key,
        model_provider="openai",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    return llm


def main():
    try:
        #初始化客户端
        llm = init_llm_client()
        logger.info("LLM客户端初始化成功")
        #普通模式调用大模型
        question = "你是谁"
        response = llm.invoke(question)

        logger.info(f"问题：{question}")
        logger.info(f"回答：{response.content}")

        print("====================以下是流式输出,另一种调用方式")
        print("*" * 50)
        #流式模式调用大模型
        response_stream = llm.stream(question)
        for chunk in response_stream:
            print(chunk.content,end="")

    #捕获具体异常
    except ValueError as e:
        logger.error(f"配置错误：{e}")
    except LangChainException as e:
        logger.error(f"模型调用失败：{e}")
    except Exception as e:
        logger.error(f"未知错误：{e}")


if __name__ == '__main__':
    main()

