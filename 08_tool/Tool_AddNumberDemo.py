from langchain.tools import tool
from langchain_core.tools import StructuredTool


@tool
def add_number(a: int,b: int)->int:
    """两个整数相加"""
    return a+b

result = add_number.invoke({"a": 1,"b": 2})

print(f"{add_number.name=}\n{add_number.description=}\n{add_number.args=}")