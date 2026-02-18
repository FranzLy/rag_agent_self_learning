from langchain_core.output_parsers import StrOutputParser
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

result = vector_store.similarity_search(
    input_text,
    2
)

reference_text = "["
for doc in result:
    reference_text += doc.page_content + ","
reference_text += "]"

def print_prompt(prompt):
    print(prompt)
    print("="*20)
    return prompt

# chain
chain = prompt | print_prompt | model | StrOutputParser()

res = chain.invoke({"input": input_text, "context": reference_text})
print(res)

