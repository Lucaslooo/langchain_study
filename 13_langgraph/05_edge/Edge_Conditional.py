from typing import Optional

from langgraph.constants import END, START
from langgraph.graph import StateGraph
from loguru import logger
from pydantic import BaseModel

"""
LangGraph 条件边
分支流程控制语句分支路由（Router → Weather / Chat）
使用langgraph构建了一个状态图，根据输入数值的奇偶性执行不同节点。
check_x接收并传递状态，
is_even判断奇偶，
handle_even和handle_odd分别处理偶数和奇数情况，最终输出结果。
"""
class MyState(BaseModel):
    """
        定义状态模型，用于在图节点之间传递数据
        Attributes:
            x (int): 输入的整数
            result (Optional[str]): 处理结果，可为"even"或"odd"
        """
    x: int
    result: Optional[str] = None

# 检查输入状态的节点函数
def check_x(state: MyState)->MyState:
    logger.info(f"[check_x] Received state: {state}")
    return state
# 判断状态中x值是否为偶数的条件函数
def is_even(state: MyState)->bool:
    return state.x % 2 == 0
#处理偶数情况的节点函数
def handle_even(state: MyState)->MyState:
    logger.info("[handle_even] x 是偶数")
    return MyState(x=state.x,result="even")
# 处理奇数情况的节点函数
def handle_odd(state: MyState)->MyState:
    logger.info("[handle_odd] x 是奇数")
    return MyState(x=state.x,result="odd")

#创建图
builder = StateGraph(MyState)
#添加节点
builder.add_node("check_x",check_x)
builder.add_node("handle_even",handle_even)
builder.add_node("handle_odd",handle_odd)

#添加起始边，流向check_x
builder.add_edge(START,"check_x")
#添加条件边，根据is_even函数的返回，来决定流向哪个节点。例子：True：handle_evnt; False：handle_odd
builder.add_conditional_edges("check_x",is_even,{
    True: "handle_even",
    False: "handle_odd"
})
#添加结束边，流向结束节点
builder.add_edge("handle_even",END)
builder.add_edge("handle_odd",END)
#构建图
graph = builder.compile()
print(graph.get_graph().print_ascii())

# logger.info("输入 x=4（偶数）")
# graph.invoke({"x":4})


logger.info("输入 x=3（奇数）")
graph.invoke({"x":3})