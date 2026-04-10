"""
把文本转换成向量有什么用呢？
最核心的作用是可以通过向量之间的计算，来分析文本与文本之间的相似性。
计算的方法有很多种，其中用得最多的是向量余弦相似度。
Python语言中提供了一个库sklearn，可以很方便的计算向量之间的余弦相似度
"""
import os
from http import HTTPStatus

import dashscope
import numpy as np
from dotenv import load_dotenv

load_dotenv()
texts = [
    '我喜欢吃苹果',
    '苹果是我最喜欢吃的水果',
    '我喜欢用苹果手机'
]
# 获取每个文本的embedding向量
embeddings = []

#将文本数组中毒每个文本进行向量化，如果向量化成功，就存入embeddings列表
for text in texts:
    input_data = [{'text': text}]
    resp = dashscope.MultiModalEmbedding.call(
        model="multimodal-embedding-v1",
        api_key=os.getenv("API_KEY"),
        input=input_data
    )
    if resp.status_code == HTTPStatus.OK:
        # 从返回结果里提取第一条文本的向量
        embedding = resp.output['embeddings'][0]['embedding']
        # 把向量存入 embeddings 列表，最终得到所有文本的向量
        embeddings.append(embedding)


#计算余弦相似度
def cosine_similarity(embedding1, embedding2):
    # 计算两个向量的余弦相似度
    dot_product = np.dot(embedding1, embedding2)
    norm_vec1 = np.linalg.norm(embedding1)
    norm_vec2 = np.linalg.norm(embedding2)
    return dot_product / (norm_vec1 * norm_vec2)


# 比较所有文本之间的相似度
print("文本相似度比较结果:")
print("=" * 60)

for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        similarity = cosine_similarity(embeddings[i], embeddings[j])
        print(f"文本{i + 1} vs 文本{j + 1}:")
        print(f"  文本{i + 1}: {texts[i]}")
        print(f"  文本{j + 1}: {texts[j]}")
        print(f"  余弦相似度: {similarity:.4f}")
        print("-" * 40)
