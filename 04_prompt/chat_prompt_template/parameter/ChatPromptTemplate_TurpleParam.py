from langchain_core.prompts import ChatPromptTemplate

chat_prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个AI开发工程师，你的名字是{name}"),
        ("human", "你能帮我做什么？"),
        ("ai", "我能帮你做很多{thing}"),
        ("human", "{input}")
    ]
)

params = {
    "name": "小文",
    "thing": "数学题",
    "input": "5+2=？"
}

prompt = chat_prompt_template.format_messages(**params)

print(prompt)
print(type(prompt))
