from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="deepseek-r1:7b",
    base_url="http://localhost:11434",
    reasoning="False"
)

print(llm.invoke("你是谁").content)
response = llm.stream("推荐一下江浙沪三月旅游攻略")
for chunk in response:
    print(chunk.content, end="")
