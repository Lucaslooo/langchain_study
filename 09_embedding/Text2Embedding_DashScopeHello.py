import os
from http import HTTPStatus
import dashscope
from dotenv import load_dotenv

load_dotenv()

input_text = "商品质量很好"

resp = dashscope.TextEmbedding.call(
    model="text-embedding-v3",
    input=input_text,
    api_key=os.getenv("API_KEY")
)

if resp.status_code == HTTPStatus.OK:
    print(resp)
