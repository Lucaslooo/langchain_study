import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#第一版 硬编码写死
# llm = ChatOpenAI(
#     model="qwen3.5-plus",
#     api_key="sk-7aa7b3791efd4260b2fee14e8c3bde43",
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )


#第二版 配置文件中读取
load_dotenv(encoding="UTF-8")
llm = ChatOpenAI(
    model=os.getenv("QWEN_MODEL"),
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

response = llm.invoke("你是谁？")  #元数据，里面可以记录使用的token
print(response)
print()
print(response.content)

# def invoke(
#         self,
#         input: LanguageModelInput,
#         config: RunnableConfig | None = None,
#         *,   * 表示：它后面的所有参数，必须用 关键字=值 的形式传入，不能直接写值。
#         stop: list[str] | None = None,
#         **kwargs: Any,   这个是关键字可变参数，接受关键字参数变成字典
# )

#  *args  这个是接收无名参数变成元组
