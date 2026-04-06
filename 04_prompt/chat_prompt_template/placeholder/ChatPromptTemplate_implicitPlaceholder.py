from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

"""
"placeholder" 是 ("placeholder", "{memory}") 的简写语法，
等价于 MessagesPlaceholder("memory")。

隐式使用MessagesPlaceholder
"""
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个ai助手，名字叫{name}"),
        # 占位符，用于插入对话“记忆”内容，即之前的聊天记录（历史上下文）
        ("placeholder", "{memory}"),
        ("human", "请问，{input}")
    ]
)

prompt = chat_prompt_template.invoke(
    {
        "name": "小文",
        # memory：是之前的对话上下文，会被插入到 {memory} 的位置
        "memory": [
            SystemMessage(content="今天天气怎么样"),
            HumanMessage(content="你真帅")
        ],
        "input": "7+2=？"
    }
)

print(prompt.to_string())
