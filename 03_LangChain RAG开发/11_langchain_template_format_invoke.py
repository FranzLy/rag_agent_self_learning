from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate

"""
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate  -> RunnableSerializable -> Runnable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate  -> RunnableSerializable -> Runnable
Tongyi -> BaseLLM -> BaseLanguageModel -> RunnableSerializable -> Runnable
ChatTongyi -> BaseChatModel -> BaseLanguageModel -> RunnableSerializable -> Runnable
"""

template = PromptTemplate.from_template("我的邻居是{name}，喜欢{hobby}")

# format传入 key-value参数对
res = template.format(name="张大民", hobby="贫嘴")
print(res, type(res))

# invoke传入字典作为参数
res2 = template.invoke({"name": "张大民", "hobby": "贫嘴"})
print(res2, type(res2)) #text='我的邻居是张大民，喜欢贫嘴' <class 'langchain_core.prompt_values.StringPromptValue'>
print(res2.to_string())