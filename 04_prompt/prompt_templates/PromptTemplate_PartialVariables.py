#方式3：部分提示词模板(partial_variables),实例化过程中指定 partial_variables 参数
import time
from datetime import datetime

from langchain_core.prompts import PromptTemplate

#1、实例化过程中指定partial_variables 参数
template = PromptTemplate.from_template(
    template="现在时间是{time},请对我的问题给出答案，我的问题是：{question}",
    partial_variables={"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
)

prompt = template.format(question="今天日期是几号？")
print(prompt)

time.sleep(2)

#2、使用partial方法指定默认值
template2 = PromptTemplate.from_template(template="现在时间是{time}，请对我的问题给出答案，我的问题是：{question}")
partial = template2.partial(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
prompt2 = partial.format(question="今天天气怎么样")

print(prompt2)

template3 = PromptTemplate(
    template="{foo} {bar}",  #str
    input_variables=["foo", "bar"],  #列表
    partial_variables={"foo": "hello"}  #预先定义部分变量为hello  #字典
)
prompt3 = template3.format(foo="lisi", bar="world")
print(prompt3)

prompt4 = template3.format(bar="world")
print(prompt4)
