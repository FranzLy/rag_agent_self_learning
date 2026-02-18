from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请帮忙起名字，"
    "并封装为JSON格式返回给我。要求key是name，value就是你起的名字，请严格遵守格式要求。"
)

llm = ChatOllama(model="qwen2.5:14b")

json_parser = JsonOutputParser() #可以使AIMessage转化为dict

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

chain = first_prompt | llm | json_parser
res = chain.invoke({"lastname":"李", "gender":"儿子"})
print(res, type(res)) #{'name': '李明瑞'} dict

chain = first_prompt | llm | json_parser | second_prompt | llm
res = chain.invoke({"lastname":"李", "gender":"儿子"})
print(res.content)
