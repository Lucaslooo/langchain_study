import os

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore

load_dotenv()

embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("API_KEY")
)

texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机",
]

embeddings = embeddingsModel.embed_documents(texts)

for i, vec in enumerate(embeddings, 1):
    print(f"文本 {i}: {texts[i - 1]}")
    print(f"向量长度: {len(vec)}")
    print(f"前5个向量值: {vec[:10]}\n")

metadata = [{"segment_id": "1"}, {"segment_id": "2"}, {"segment_id": "3"}]
redis_url = os.getenv('REDIS_URL')
redis_config = RedisConfig(
    index_name="newsgroups",
    redis_url=redis_url
)

vector_store = RedisVectorStore(embeddingsModel, redis_config)

ids = vector_store.add_texts(texts, metadata)

print(ids[0:5])
