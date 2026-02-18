from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen2.5:14b")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业地回答用户问题。参考资料：{context}。"),
        ("user", "用户提问：{input}")
    ]
)

vector_store = InMemoryVectorStore(
    embedding=HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5"
    )
)

# 准备一下资料（向量库的数据）
# add_texts 传入一个list[str]
vector_store.add_texts(
    ["减肥就是要少吃多练", "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"]
)

input_text = "怎么减肥？"


# result = vector_store.similarity_search(
#     input_text,
#     2
# )
#
# reference_text = "["
# for doc in result:
#     reference_text += doc.page_content + ","
# reference_text += "]"


def print_prompt(prompt):
    print(prompt)
    print("=" * 20)
    return prompt


# langchain 中向量存储对象，有一个方法：as_retriever，可以返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k": 2})


def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料"

    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content + ","
    formatted_str += "]"
    return formatted_str


# chain
chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
)
"""
retriever:
    - 输入：用户的提问       str
    - 输出：向量库的检索结果  list[Document]
prompt:
    - 输入：用户的提问 + 向量库的检索结果   dict
    - 输出：完整的提示词                 PromptValue
"""

res = chain.invoke(input_text)
print(res)
