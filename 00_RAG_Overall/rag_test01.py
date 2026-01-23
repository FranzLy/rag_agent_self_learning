from operator import itemgetter
from pathlib import Path

import langchain_core.documents
from langchain_community.document_loaders import TextLoader, DirectoryLoader, WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# 1. 设置模型
llm = ChatOpenAI(model="gpt-4.1-mini")
embedding_model = HuggingFaceEmbeddings(model_name = "./models/bge-large-zh-v1.5")

# 2. 设置数据处理（加载 分块 存储 检索）
file_dir = Path('./knowledge')
text_spliter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap=100) # 采用滑动窗口分块
vector_store = Chroma(embedding_function = embedding_model, persist_directory = "./chroma_v3")
retriever = vector_store.as_retriever(search_kwargs={"k":5})

# 3. 初始化数据库，初始一次
docs = DirectoryLoader(str(file_dir), loader_cls = TextLoader).load() #加载文档
docs = text_spliter.split_documents(docs) #切分文档
vector_store.add_documents(docs) #存储文档

# 4. 提示词模版
prompt_template = PromptTemplate.from_template("""
你是一个严谨的RAG助手。
请根据以下提供的上下文信息来回答问题。
如果上下文信息不足以回答问题，请直接说“根据提供的信息无法回答”。
如果回答时间使用了上下文中的嘻嘻，在回答后输出使用了哪些上下文，
上下文信息：
{context}
------------
问题：{question}
""")

# 5. 编排“链”
chain = {"question": RunnablePassthrough()} | RunnablePassthrough.assign(context=itemgetter("question") | retriever) | prompt_template | llm | StrOutputParser()

# 6. 提问
print(chain.invoke("共有多少种飞行器？"))