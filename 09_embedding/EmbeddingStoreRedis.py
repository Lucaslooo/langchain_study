import os

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.documents import Document

load_dotenv()
embedding = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("API_KEY")
)

texts = [
    "通义千问是阿里巴巴研发的大语言模型。",
    "Redis 是一个高性能的键值存储系统，支持向量检索。",
    "LangChain 可以轻松集成各种大模型和向量数据库。"
]

#把纯文本列表，包装成 LangChain 专用的 Document 文档列表。  page_content：文本内容;    metadata：附加信息（source：来源字段，"manual"：表示来自 “手动录入 / 手册”）
#为什么要转成 Document？ 用于后续 RAG、向量检索、文档分割、存入向量库
documents = [Document(page_content=text, metadata={"source": "manual"}) for text in texts]
redis_url = os.getenv('REDIS_URL')
vector_store = Redis.from_documents(
    documents=documents,
    embedding=embedding,
    redis_url=redis_url,
    index_name="my_index11"  #创建向量索引
)
#创建检索器,k=2 = 每次只返回最相关的 2 条结果
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
#开始检索，提问
results = retriever.invoke("LangChain 和 Redis 怎么结合？")
for res in results:
    print(res.page_content)

"""
流程：
把你的问题转成向量
去 Redis 里找向量最接近的文档
返回最相似的文档列表
"""
