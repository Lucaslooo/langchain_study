from langchain_core.prompts import PromptTemplate

#分别创立两个独立的提示词模板
template_a = PromptTemplate.from_template("请用一句话介绍{topic},要求通俗易懂\n")
template_b = PromptTemplate.from_template("要求内容不超过：{length}字")
#将两个模板进行拼接整合
template_all = template_a + template_b
#填充组合后，生成最后的提示词
prompt = template_all.format(topic="langchain", length="200")

print(prompt)
