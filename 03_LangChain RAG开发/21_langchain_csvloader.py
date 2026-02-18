from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",
    csv_args={
        "delimiter": ",", # 指定分隔符
        "quotechar": '"',
        "fieldnames": ["name", "age", "gender", "hobby"]
    }
)

# 批量加载 .load()   ->  [Document, Document, ...]
# documents = loader.load()
#
# for document in documents:
#     print(type(document), document)

# 懒加载 .lazy_loader() 迭代器[Document]
for documents in loader.lazy_load():
    print(documents)