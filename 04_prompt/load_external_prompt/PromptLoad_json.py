
from langchain_core.prompts import load_prompt

template = load_prompt("prompt.json", encoding="utf-8")  #load_prompt() 这个函数已经被官方废弃了，未来2.0版本会删掉！


print(template.format(name="张三", what="搞笑的"))
