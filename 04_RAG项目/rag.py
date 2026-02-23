from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from vector_stores import VectorStoreService
from chat_history_store import get_history

import config_data as config


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=HuggingFaceEmbeddings(
                model_name=config.embedding_model_name,
            )
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，简洁和专业地回答用户问题，参考资料：{context}。"),
                ("system", "以及用户的提问历史记录：{history}"),
                ("user", "请回答用户问题：{input}")
            ]
        )

        self.chat_model = ChatOllama(
            model=config.chat_model_name,
        )

        self.chain = self.__get_chain()

    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()

        def format_for_retriever(value: dict) -> str:
            print(value)
            return value["input"]

        def format_document(docs: list[Document]) -> str:
            if not docs:
                return "无相关参考资料"

            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str

        def format_for_prompt(value: dict) -> dict:
            print(value)
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["history"] = value["input"]["history"]
            new_value["context"] = value["context"]
            return new_value

        def print_prompt(prompt):
            print("=" * 20)
            print(prompt)
            print("=" * 20)
            return prompt

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(format_for_retriever) | retriever | format_document
                }
                | RunnableLambda(format_for_prompt) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain


if __name__ == '__main__':
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
    res = RagService().chain.invoke({"input": "针织衫如何保养？"}, session_config)
    print(res)
