from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(template="你的角色是{role},我的问题是{question}")
prompt = template.format(role="python工程师", question="今天天气怎么样")
print(prompt)
print(type(prompt))
print()
