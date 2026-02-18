from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

prompt_template = PromptTemplate.from_template("你是一个AI助手")

llm = OllamaLLM(model="qwen2.5:14b")

"""<class 'langchain_core.runnables.base.RunnableSequence'>"""
chain = prompt_template | llm
print(type(chain))