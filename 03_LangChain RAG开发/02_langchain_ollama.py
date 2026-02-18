from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model = "qwen2.5:14b"
)

res = llm.invoke(input="你是谁？")

print(res)