from .path_tools import get_abs_path
from .config_handler import prompts_config
from .logger_handler import logger

def load_system_prompt():
    try:
        system_prompt_path=get_abs_path(prompts_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompt]解析系统提示词文件路径失败")
        raise e

    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error(f"[load_system_prompt]系统提示词文件{system_prompt_path}不存在")
        raise e
    except Exception as e:
        logger.error(f"[load_system_prompt]解析系统提示词文件{system_prompt_path}失败")
        raise e

def load_rag_prompt():
    try:
        rag_prompt_path = get_abs_path(prompts_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompt]解析RAG提示词文件路径失败")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error(f"[load_rag_prompt]RAG提示词文件{rag_prompt_path}不存在")
        raise e
    except Exception as e:
        logger.error(f"[load_rag_prompt]解析RAG提示词文件{rag_prompt_path}失败")
        raise e

def load_report_prompt():
    try:
        report_prompt_path = get_abs_path(prompts_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompt]解析系统提示词文件路径失败")
        raise e

    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except FileNotFoundError as e:
        logger.error(f"[load_report_prompt]系统提示词文件{report_prompt_path}不存在")
        raise e
    except Exception as e:
        logger.error(f"[load_report_prompt]解析系统提示词文件{report_prompt_path}失败")
        raise e

if __name__ == '__main__':
    print(load_system_prompt())
    print(load_rag_prompt())
    print(load_report_prompt())
