import os

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_redis import RedisVectorStore, RedisConfig

load_dotenv()

embeddingModel = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("API_KEY")
)

redis_config = RedisConfig(
    redis_url=os.getenv("REDIS_URL"),
    index_name="newsgroups"   #Redis 向量数据库是按索引（index）存储的;一个数据库 = 多个文件夹,index_name = 文件夹名
)

query = "我喜欢用什么手机？"
#2. 创建Redis向量存储实例
vector_store = RedisVectorStore(embeddingModel, redis_config)
#3. 将查询语句向量化，并在Redis中做相似度检索
results = vector_store.similarity_search_with_score(query, k=2)

print("=== 查询结果 ===")
#results：向量库返回的 检索结果列表; doc：查到的 文档对象; score：向量之间的 距离分数; enumerate(results, 1)：从 1 开始编号（结果 1、结果 2…）
for i, (doc, score) in enumerate(results, 1):
    similarity = 1 - score  #  score 是距离，可以转成相似度
    print(f"结果 {i}:")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
    print(f"相似度: {similarity:.4f}")
