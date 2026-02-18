from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="./data/stu.json",
    jq_schema=".name",
    text_content=True,  # 告知JSONLoader 我抽取的内容不是字符串
    json_lines=False  # 告知JSONLoader 这是一个JSONLines文件（每一行都是一个独立的标准JSON）
)

document = loader.load()
print(document)
print(document[0].page_content)

print("="*20)

loader2 = JSONLoader(
    file_path="./data/stus.json",
    jq_schema=".[].name",
    text_content=False,
)

document = loader2.load()
print(document)
for doc in document:
    print(doc.page_content)

print("="*20)

loader3 = JSONLoader(
    file_path="./data/stus_json_lines.json",
    jq_schema=".name",
    text_content=False,
    json_lines=True
)

document = loader3.load()
for doc in document:
    print(doc.page_content)
