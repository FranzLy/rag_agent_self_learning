from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

chat_prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个边塞诗人，可以作诗。"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首唐诗"),
    ]
)

history_data = [
    ("human", "你来写一个唐诗"),
    ("ai", "床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human", "好诗再来一个"),
    ("ai", "锄禾日当午，汗滴禾下锄，谁知盘中餐，粒粒皆辛苦"),
]

prompt_text = chat_prompt_template.invoke({"history": history_data})
""" type:class 'langchain_core.prompt_values.ChatPromptValue' """
print(prompt_text, type(prompt_text))
print(prompt_text.to_string())


llm = ChatOllama(model="qwen2.5:14b")
res = llm.invoke(prompt_text)
print(res.content)
print(type(res)) #langchain_core.messages.ai.AIMessage