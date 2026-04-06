from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

"""
message 类型

System/Human/AIMessage 是 langchain 中用于构建不同角色的一个类。
它通常用于创建聊天消息的一部分，特别是当你构建一个多轮对话的 prompt 模板时，区分系统、AI、和人类消息
"""

# 创建聊天提示模板，用于构建AI助手的对话上下文
# 该模板包含两个消息：AI助手的自我介绍和用户问题
chat_prompt_template = ChatPromptTemplate(
    [
        SystemMessage(content="你是一个ai助手，你的名字是{name}"),
        HumanMessage(content="请回答：{input}")
    ]
)

prompt = chat_prompt_template.format_messages(name="小文", input="今天天气怎么样？")
print(prompt)
