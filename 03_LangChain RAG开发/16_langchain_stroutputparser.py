from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

parser = StrOutputParser() #可以将AIMessage转换为基础字符串，并加入chain作为组件存在
prompt_template = PromptTemplate.from_template(
    "我的邻居姓：{lastname}, 刚生了{gender}, 请起个名字，简单回答。"
)

llm = ChatOllama(model="qwen2.5:14b")

chain = prompt_template | llm | parser | llm
res: AIMessage = chain.invoke({"lastname": "李", "gender": "女儿"})
print(res.content, type(res)) # type = AIMessage

print("="*100)
chain = chain | parser
res = chain.invoke({"lastname": "李", "gender": "女儿"})
print(res, type(res)) # type = str
