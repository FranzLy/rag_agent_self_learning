from ftplib import print_line

from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model = "qwen2.5:14b"
)


res = llm.stream(input="你是谁，可以做什么？") #stream是流式方法， invoke是全部输出

for chunk in res:
    print(chunk, end="", flush=True)

print_line('\n')
print("="*100)

llm2 = OllamaLLM(
    model = "llama3.1:8b"
)

res2 = llm2.stream(input="你是谁？") #stream是流式方法， invoke是全部输出

for chunk in res2:
    print(chunk, end="", flush=True)
