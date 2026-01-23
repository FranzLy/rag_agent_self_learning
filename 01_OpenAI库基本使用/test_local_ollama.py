from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:11434/v1",
)

completion = client.chat.completions.create(
    model="qwen2.5:14b",
    messages=[
        {"role": "system", "content":"你是一名Python编程专家，不说废话简单回答"}, # 设定模型的行为和规则
        {"role": "assistant", "content": "好的，我是编程专家，话不多，你要问什么？"}, # 设定模型的回答，由用户设定
        {"role": "user", "content": "输出1-10的数字，使用Python"} # 用户的提问
    ],
    stream = True
)

# print(completion.choices[0].message.content)

for chunk in completion:
    print(chunk.choices[0].delta.content, end="", flush=True)