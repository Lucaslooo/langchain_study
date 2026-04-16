from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
"""
OverallState：图内部流转的完整状态
input_schema=InputState：
✅ 外部调用图时，只能传 question
✅ 传别的 key 会直接报错
output_schema=OutputState：
✅ 图执行完，只返回 answer
✅ 自动过滤掉内部的 question 等中间字段
"""

class InputState(TypedDict):
    question:str

class OutputState(TypedDict):
    answer:str

class OverAllState(TypedDict):
    pass  #空语句，为了让语法不报错

def answer_node(state: InputState):
    """
    处理输入并生成答案的节点
    Args:
        state: 输入状态
    Returns:
        dict: 包含答案的字典
    """
    print(f"执行 answer_node 节点:")
    print(f"  输入: {state}")

    # 示例答案
    answer = "再见" if "bye" in state["question"].lower() else "你好"
    result = {"answer": answer, "question": state["question"]}

    print(f"  输出: {result}")
    return result

def demo_input_output_schema():
    """演示输入输出模式"""
    print("=== 演示输入输出模式 ===")

    graph = StateGraph(OverAllState,input_schema=InputState,output_schema=OutputState)

    graph.add_node("answer_node",answer_node)

    graph.add_edge(START,"answer_node")
    graph.add_edge("answer_node",END)

    app = graph.compile()

    result = app.invoke({"question":"你好"})
    print(f"图调用结果: {result}")
    # 打印图的ascii可视化结构
    print(app.get_graph().print_ascii())
    print()

def main():
    """主函数"""
    print("=== LangGraph 图输入输出模式===\n")

    # 演示输入输出模式
    demo_input_output_schema()

    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()