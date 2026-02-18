from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "qwen2.5:14b"
)

# 简写支持变量注入
messages = [
    ("system", "你是一名初唐诗人"),
    ("human", "写一首唐诗"),
    ("ai", "锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human", "按照你上一个回复的格式，在写一首唐诗。")
]

resp = llm.stream(input=messages)

for chunk in resp:
    print(chunk.content, end="", flush=True)