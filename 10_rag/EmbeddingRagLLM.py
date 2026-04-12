import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",
         """
    请使用以下提供的文本内容来回答问题。仅使用提供的文本信息，
    如果文本中没有相关信息，请回答"抱歉，提供的文本中没有这个信息"。

    文本内容：
    {context}
    """),  # 不能使用MessagesPlaceholder(context)，因为retriever返回的是document，不是消息列表
        ("human", "{question}")
    ]
)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("API_KEY")
)
# 4. 加载文档
# 4.1 TextLoader 无法处理 .docx 格式文件，专门用于加载纯文本文件的（如 .txt）
# loader = TextLoader("alibaba-more.docx", encoding="utf-8")

# 4.2 LangChain提供了Docx2txtLoader专门用于加载.docx文件，先通过pip install docx2txt
loader = Docx2txtLoader("alibaba-java.docx")
document = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)
texts = text_splitter.split_documents(document)

redis_url = os.getenv("REDIS_URL")
redis_config = RedisConfig(
    index_name="AIOPS2",
    redis_url=redis_url
)

redis_vector_store = RedisVectorStore(embeddings, redis_config)

# ======================
# ✅ 最终正确逻辑：空则插入，不空则跳过
# 只检查当前索引 AIOPS2
# ======================
"""
情况 1：索引里 有数据 库里有一堆文档,虽然没有 “test”,但 Redis 还是会返回 最不相关的那一条,结果长度 = 1 → 我们判断：有数据，不插入
情况 2：索引 完全空,一条数据都没有,不管搜什么都返回 [],结果长度 = 0,→ 我们判断：空库，插入数据
"""
search_results = redis_vector_store.similarity_search("test", k=1)
if len(search_results) == 0:
    print("当前索引为空，开始初始化...")
    redis_vector_store.add_documents(texts)
else:
    print("当前索引已有数据，跳过插入 ✅")

retriever = redis_vector_store.as_retriever(search_kwargs={"k": 2})
"""
并行获取 {上下文 + 问题}
→ 塞进提示词模板 prompt
→ 丢给大模型 llm 生成回答
"""
rag_chain = (
        # 管道 | 里面直接写字典 { } → 自动变成 RunnableParallel，这是一个并行链，去向量库查资料和传递用户问题并行
        {
            "context": retriever,  # 去向量库查资料
            "question": RunnablePassthrough()  #传递用户问题
        }
        | prompt_template
        | llm
)

question = "00000和A0001分别是什么意思"
#question2 = "00008分别是什么意思"
result = rag_chain.invoke(question)
print(f"问题：{question}\n")
print(f"答案：{result.content}\n")
