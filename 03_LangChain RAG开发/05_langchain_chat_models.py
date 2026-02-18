from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

llm = ChatOpenAI(
    model = "gpt-4.1-mini"
)

messages = [
    SystemMessage(content="你是一名初唐诗人"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一个回复的格式，在写一首唐诗。")
]

resp = llm.stream(input=messages)

for chunk in resp:
    print(chunk.content, end="", flush=True)