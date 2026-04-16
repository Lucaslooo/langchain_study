'''图的构建流程：
1、初始化一个StateGraph实例。
2、添加节点。
3、定义边，将所有的节点连接起来。
4、设置特殊节点，入口和出口（可选）。
5、编译图。
6、执行工作流。'''
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph

#定义状态
class GraphState(TypedDict):
    process_data: dict

#定义节点
def input_node(state: GraphState):
    print(f"input node节点执行:state.get('process_data')结果内容：{state.get('process_data')}")
    return {"process_data": {"input": "input_value"}}


def process_node(state: GraphState):
    print(f"process_node节点执行:state.get('process_data')结果内容：{state.get('process_data')}")
    return {"process_data": {"process": "input_value_11112333"}}


def output_node(state: GraphState):
    print(f"output_node节点执行:state.get('process_data')结果内容：{state.get('process_data')}")
    return {"process_data": state.get("process_data")}

#创建图并指定状态
graph = StateGraph(GraphState)
#添加节点
graph.add_node("input_node",input_node)
graph.add_node("process_node",process_node)
graph.add_node("output_node",output_node)
#添加边
graph.add_edge(START,"input_node")
graph.add_edge("input_node","process_node")
graph.add_edge("process_node","output_node")
graph.add_edge("output_node",END)
#构建图生成app
app = graph.compile()
#调用
result = app.invoke({"process_data":{"name": "测试数据", "value": 123456}})

print(result)

# 打印图的ascii可视化结构
print(app.get_graph().print_ascii())
print("=================================")
print()
# 打印图的可视化结构，生成更加美观的Mermaid 代码，通过processon 编辑器查看
print(app.get_graph().draw_mermaid())