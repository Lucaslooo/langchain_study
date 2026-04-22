from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph

#定义状态类型
class State(TypedDict):
    x: int
#定义加法节点函数加1
def addition1(state: State):
    print(f"加法节点addition1收到的初始值：{state}")
    return {"x": state["x"]+1}
#定义加法节点函数加2
def addition2(state: State):
    print(f"加法节点addition2收到的初始值：{state}")
    return {"x": state["x"]+2}
#定义加法节点函数加3
def addition3(state: State):
    print(f"加法节点addition3收到的初始值：{state}")
    return {"x": state["x"]+3}
#添加路由逻辑函数，根据输入的值，进行走不同的路由
def handle_plus(state: State)->str:
    flag = state["x"]
    if flag == 1:
        return "condition1"
    elif flag == 2:
        return "condition2"
    else:
        return "condition3"

builder = StateGraph(State)
builder.add_node("node1",addition1)
builder.add_node("node2",addition2)
builder.add_node("node3",addition3)
# 添加路由函数，参数：当前节点，路由函数，路由函数返回的条件与node的映射
builder.add_conditional_edges(START,handle_plus,{
    "condition1":"node1",
    "condition2":"node2",
    "condition3":"node3"
})
#所有处理节点都连接到END
builder.add_edge("node1",END)
builder.add_edge("node2",END)
builder.add_edge("node3",END)

graph = builder.compile()
result = graph.invoke({"x":2})

print(result)
