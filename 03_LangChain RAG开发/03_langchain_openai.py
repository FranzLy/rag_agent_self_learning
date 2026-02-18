from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "gpt-4.1-mini"
)

res = llm.invoke(input="你是谁？")

print(res)