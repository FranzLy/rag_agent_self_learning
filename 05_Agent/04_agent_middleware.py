from langchain.agents import create_agent, AgentState
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langgraph.runtime import Runtime

@tool(description="查询天气")
def get_weather() -> int:
    return "晴天"

"""
1. agent 执行前
2. agent 执行后
3. model 执行前
4. model 执行后
5. tool 执行中
6. 模型执行中
"""

@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[before agent]agent启动，并附带{len(state['messages'])}消息")

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after agent]agent结束，并附带{len(state['messages'])}消息")

@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before model]模型执行前，并附带{len(state['messages'])}消息")

@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after model]模型执行后，并附带{len(state['messages'])}消息")

@wrap_model_call
def log_wrap_model_call(request, handler):
    print(f"[wrap model call]模型执行中")

    return handler(request)

@wrap_tool_call
def log_wrap_tool_call(request, handler):
    print(f"[wrap tool call]工具执行：{request.tool_call['name']}")
    print(f"[wrap tool call]工具参数：{request.tool_call['args']}")

    return handler(request)

agent = create_agent(
    model=ChatOllama(model="qwen2.5:14b"),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，可以回答用户问题，必须始终只用简体中文回答，不得使用任何其他语言。",
    middleware=[log_before_agent, log_after_agent, log_before_model, log_after_model, log_wrap_model_call, log_wrap_tool_call]
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