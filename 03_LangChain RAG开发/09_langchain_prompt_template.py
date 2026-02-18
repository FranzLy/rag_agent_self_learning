from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# zero-shot
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚生了{gender}, 请帮忙取个名字，简单回答。"
)

# 通过format注入变量值
# prompt_text = prompt_template.format(lastname = "李", gender = "女儿")
#
llm = OllamaLLM(model = "qwen2.5:14b")
#
# res = llm.invoke(prompt_text)
# print(res)

# 通过链的方式
chain = prompt_template | llm
res = chain.invoke(input={"lastname": "李", "gender": "女儿"})
print(res)