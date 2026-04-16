import os
from typing import TypedDict, Annotated, List

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph

load_dotenv()
#1、定义状态state；存储对话信息
class LLMState(TypedDict):
    messages: Annotated[List, add_messages]

#2、定义大模型
llm = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)
#3、定义节点函数node：调用大模型，并把回复添加到messages里面
def model_node(state: LLMState):
    reply = llm.invoke(state["messages"])
    return {"messages":reply}

#4、生成图
graph = StateGraph(LLMState)
#5、图中添加节点
graph.add_node("model_node",model_node)
#6、图中添加edge（边）
graph.add_edge(START,"model_node")
graph.add_edge("model_node",END)
#7、编译图
app = graph.compile()
#8、运行
result = app.invoke({"messages":"请用一句话描述langgraph是什么？要求简短，不超过50字"})
# 打印模型的最后一条回复
print("模型回答：", result["messages"][-1].content)
print()
# =========================
#1. 打印图的ascii可视化结构
print(app.get_graph().print_ascii())
print("="*50)

#2. 打印图的Mermaid代码可视化结构并通过https://www.processon.com/mermaid编辑器查看
print(app.get_graph().draw_mermaid())
print("="*50)