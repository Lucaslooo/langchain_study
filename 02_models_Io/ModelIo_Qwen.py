import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage

# 加载环境变量
load_dotenv()

# 🔥 修复版：只保留正确参数，删掉错误的 url
chatllm = ChatTongyi(
    model_name="qwen-plus",  # 必须用这个格式
    streaming=True,
    api_key=os.getenv("API_KEY"),  # 你的 API KEY
)

# 消息必须用 LangChain 标准格式
messages = [
    SystemMessage(content="你是一名专业的翻译家，可以将用户的中文翻译为英文。"),
    HumanMessage(content="我喜欢编程。"),
]

# 流式输出
response = chatllm.stream(messages)
for chunk in response:
    print(chunk.content, end="")
