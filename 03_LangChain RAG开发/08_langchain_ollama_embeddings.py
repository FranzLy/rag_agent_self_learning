from langchain_ollama import OllamaEmbeddings

model = OllamaEmbeddings(model="qwen3-embedding:latest")

print(model.embed_query("我喜欢你")) #单词转换
print("*"*100)
print(model.embed_documents(["我喜欢你", "晚上吃啥"])) #批量转换