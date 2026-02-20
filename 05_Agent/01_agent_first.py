from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama


@tool(description="查询天气")
def get_weather() -> str:
    return "大晴天"


agent = create_agent(
    model=ChatOllama(model="qwen2.5:14b"),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，可以回答用户问题",
)

res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "明天马里兰天气如何？"},
        ]
    }
)

for msg in res["messages"]:
    print(type(msg).__name__, msg.content)
