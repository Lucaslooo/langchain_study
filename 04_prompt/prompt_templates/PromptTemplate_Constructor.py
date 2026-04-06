import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

"""
构造器生成提示词模板
"""
load_dotenv()
prompt_template = PromptTemplate(
    template="你是一名{role},请回答我的问题，然后给出回答，我的问题是{question}",
    input_variables="role,question"
)

prompt = prompt_template.format(role="python程序员", question="写出冒泡排序的算法，只要代码")

print(prompt)

# llm = init_chat_model(
#     model="qwen3.6-plus",
#     api_key=os.getenv("API_KEY"),
#     model_provider="openai",
#     base_url=os.getenv("BASE_URL")
# )
#
# response = llm.invoke(prompt)
# print(response.content)

prompt_template2 = PromptTemplate(
    template="帮我整理出商品{product}的优缺点，包括{aspect1}和{aspect2}",
    input_variables="product,aspect1,aspect2"
)

product_prompt = prompt_template2.format(product="小米汽车", aspect1="电池续航", aspect2="安全系数")
print(product_prompt)
