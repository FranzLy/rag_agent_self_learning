from langchain.agents import AgentState
from langgraph.runtime import Runtime
from langgraph.types import Command
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable, Any
from langchain_core.messages import ToolMessage
from utils import logger, load_report_prompt, load_system_prompt

from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest


@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    logger.info(f"Monitoring tool: 执行工具 {request.tool_call['name']}")
    logger.info(f"Monitoring tool: 执行工具参数 {request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"Monitoring tool工具：{request.tool_call['name']}调用成功")

        if request.tool_call['name'] == 'fill_context_for_report':
            logger.info(f"Monitoring tool: fill_context_for_report工具被调用，注入上下文 report = True")
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.info(f"工具{request.tool_call['name']}调用失败：{e}")
        raise


@before_model
def log_before_model(
        state: AgentState,  # 整个Agent智能体中的状态记录
        runtime: Runtime  # 记录整个执行过程中的上下文信息
) -> dict[str, Any] | None:
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息")

    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content}")

    return None


@dynamic_prompt  # 每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):  # 动态切换提示词
    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompt()

    return load_system_prompt()
