import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_ollama import ChatOllama


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id  # 会话id
        self.storage_path = storage_path  # 不同会话id的存储文件，所在的文件夹路径

        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)
        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列 类似list、tuple
        all_messages = list(messages)  # 已有的消息列表
        all_messages.extend(messages)  # 新的和已有的融合成一个list

        # 将数据同步写入到本地文件中
        # 类对象写入文件 -> 一堆二进制
        # 为了方便，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
        # 官方message_to_dict：单个消息对象（BaseMessage类实例） -> 字典
        new_messages = [message_to_dict(message) for message in all_messages]
        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    @property  # @property装饰器将messages方法变成成员属性用
    def messages(self) -> list[BaseMessage]:
        # 当前文件内： list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)  # 返回值就是：list[字典]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


llm = ChatOllama(
    model="qwen2.5:14b"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")

    ]
)

str_parser = StrOutputParser()


def print_prompt(full_prompt):
    print("=" * 20, full_prompt, "=" * 20)
    return full_prompt


base_chain = prompt | print_prompt | llm | str_parser


def get_hisotry(session_id):
    return FileChatMessageHistory(session_id, os.path.join(session_id, "./chat_history"))


conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_hisotry,
    input_messages_key="input",
    history_messages_key="chat_history"
)

if __name__ == "__main__":
    session_config = {
        "configurable": {
            "session_id": "user_id"
        }
    }
    #
    # res = conversation_chain.invoke({"input": "小明有2个猫"}, session_config)
    # print("第一次执行：", res)
    #
    # res = conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    # print("第二次执行：", res)

    res = conversation_chain.invoke({"input": "总共有几个宠物"}, session_config)
    print("第三次执行：", res)