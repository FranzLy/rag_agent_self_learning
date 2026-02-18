from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama

first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请帮忙起一个名字，仅给出名字。"
)

llm = ChatOllama(model="qwen2.5:14b")

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

# 函数的入参：AIMessage -> dict  ({"name": "xxx"})
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})
# chain = first_prompt | llm | my_func | second_prompt | llm

chain = first_prompt | llm | (lambda ai_msg: {"name": ai_msg.content}) | second_prompt | llm
res = chain.invoke({"lastname":"李", "gender":"儿子"})
print(res.content)
