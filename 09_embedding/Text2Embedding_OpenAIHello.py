import os

from dotenv import load_dotenv
from openai import OpenAI

input_text = "衣服质量非常好"
load_dotenv()
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.embeddings.create(
    model="text-embedding-v3",
    input=input_text,
)

print(completion.model_dump_json())
