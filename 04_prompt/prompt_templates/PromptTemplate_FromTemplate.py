import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

'''
FromTemplate 生成提示词模板
'''

load_dotenv()

llm = init_chat_model(
    model="qwen3.5-flash",
    api_key=os.getenv("API_KEY"),
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 使用from_template生成提示词模板
template = PromptTemplate.from_template("请给我一个关于{topic}的{type}解释")
#提示词模板使用format生成提示词
prompt = template.format(topic="量子力学", type="简短")
print(prompt)

response = llm.stream(prompt)
for chunk in response:
    print(chunk.content, end="")
