from typing import TypedDict

from langgraph.graph import StateGraph, START, END


#1、定义state
class HelloState(TypedDict):
    name: str
    greeting: str


#2、定义node节点
def greeting(hello_state: HelloState) -> dict:
    name = hello_state["name"]
    return {"greeting": f"Hello, {name}!"}


def add_emoji(hello_state: HelloState) -> dict:
    greet = hello_state["greeting"]
    return {"greeting": greet + "  。。。😄"}

#构建图graph
graph = StateGraph(HelloState)

#往图里添加node
graph.add_node("greeting", greeting)
graph.add_node("add_emoji", add_emoji)
#往图里添加edge(边)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "add_emoji")
graph.add_edge("add_emoji", END)
#4、编译图
app = graph.compile()
#5、运行
# invoke()方法只接收状态字典作为核心参数
result = app.invoke({"name": "z3"})
print(result)
print(result["greeting"])

#
# #6 打印图的边和节点信息
#6.1 打印图的ascii可视化结构
print(app.get_graph().print_ascii())
print("=" * 50)
#
# #6.2 打印图的Mermaid代码可视化结构并通过https://www.processon.com/mermaid编辑器查看
print(app.get_graph().draw_mermaid())
print("=" * 50)

#
# #6.3 生成 PNG并写入文件
# png_bytes = app.get_graph().draw_mermaid_png(max_retries=2,retry_delay=2.0)
# output_path = "langgraph" + str(uuid.uuid4())[:8] + ".png"
# with open(output_path, "wb") as f:
#     f.write(png_bytes)
# print(f"图片已生成：{output_path}")

"""
上面第3种方式，容易bug,时好时坏
ValueError: Failed to reach https://mermaid.ink  API while trying to render your graph after 1 retries. 
To resolve this issue:
1. Check your internet connection and try again
2. Try with higher retry settings: `draw_mermaid_png(..., max_retries=5, retry_delay=2.0)`
3. Use the Pyppeteer rendering method which will render your graph locally in a browser: 
`draw_mermaid_png(..., draw_method=MermaidDrawMethod.PYPPETEER)`
"""
