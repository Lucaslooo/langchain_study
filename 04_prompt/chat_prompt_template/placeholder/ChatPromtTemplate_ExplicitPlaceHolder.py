from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

"""
如果我们不确定消息何时生成，也不确定要插入几条消息，比如在提示词中添加聊天历史记忆这种场景，
可以在ChatPromptTemplate添加MessagesPlaceholder占位符，在调用invoke时，在占位符处插入消息。

显式使用MessagesPlaceholder
"""
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个ai助手，名字叫{name}"),
        # 插入 memory 占位符，用于填充历史对话记录（如多轮对话上下文）
        MessagesPlaceholder("memory"),
        ("human", "请问：{question}")
    ]
)
#MessagesPlaceholder 里面只接受消息对象列表，不能写字典格式
# 调用 prompt.invoke 来格式化整个 Prompt 模板
# 传入的参数中：
# - memory：是一组历史消息，表示之前的对话内容（多轮上下文）
# - question：是当前用户的问题
prompt = chat_prompt_template.invoke(
    {
        "name": "小文",
        "memory": [
            # 用户第一轮说的话
            SystemMessage(content="很高兴遇见你，1111"),
            # AI 第一轮的回应
            HumanMessage(content="今天天气怎么样?")
        ],
        "question": "7+2=？"
    }
)

print(prompt.to_string())
