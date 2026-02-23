from datetime import datetime
import logging
import os
from typing import Optional

from .path_tools import get_abs_path

# 日志保存的根目录
LOG_ROOT = get_abs_path('logs')

# 确保日志的目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式配置 （error info debug）
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file: Optional[str] = None
) -> logging.Logger:
    # 1. 创建/获取日志器
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # 全局最低级别

    """避免重复添加Handler"""
    if logger.handlers:
        return logger

    # 控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)

    #     文件handler
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger


# 快捷获取默认agent日志器
logger = get_logger("agent")

if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("error日志")
    logger.warning("warn日志")
    logger.debug("debug日志")
