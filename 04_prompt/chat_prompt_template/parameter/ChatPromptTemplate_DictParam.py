from langchain_core.prompts import ChatPromptTemplate
"""
列表参数格式是dict类型

	dict 构成的列表，格式为[{“role”:... , “content”:...}]
chat_prompt = ChatPromptTemplate(
    [
        {"role": "system", "content": "你是AI助手，你的名字叫{name}。"},
        {"role": "user", "content": "请问：{question}"}
    ]
)
"""
chat_prompt_template = ChatPromptTemplate(
    [
        {
            "role": "system",
            "content": "你是一个ai助手，名字是{name}，你能帮我做什么{thing}",
        },
        {
            "role": "human",
            "content": "{input}"
        }
    ]
)

prompt = chat_prompt_template.format_messages(name="小文", thing="数学题", input="你能帮我做什么？")
print(prompt)
print(type(prompt))
