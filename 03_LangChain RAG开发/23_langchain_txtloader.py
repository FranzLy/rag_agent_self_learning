from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="./data/Python基础语法.txt",
    encoding="utf-8"
)

docs = loader.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    # 文本自然段落分隔的依据符号
    separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
    length_function=len,    #统计字符的依据函数
)

split_docs = splitter.split_documents(docs)
print(len(split_docs))
for s in split_docs:
    print("="*20)
    print(s)
    print("="*20)

