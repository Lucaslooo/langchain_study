from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class HelloState(TypedDict):
    name: str
    greeting: str


def greeting(hello_state:HelloState) -> dict:
    name = hello_state["name"]
    return {"greeting":f"Hello, {name}!"}

def add_emoji(hello_state:HelloState) -> dict:
    greet = hello_state["greeting"]
    return {"greeting": greet + "  。。。😄"}

graph = StateGraph(HelloState)

graph.add_node("greeting", greeting)
graph.add_node("add_emoji", add_emoji)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "add_emoji")
graph.add_edge("add_emoji", END)

app = graph.compile()

result = app.invoke({"name":"z3"})
print(result)
print(result["greeting"])