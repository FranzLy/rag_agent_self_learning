from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
)

responses = client.chat.completions.create(
    model="qwen2.5:14b",
    messages=[
        {"role": "system", "content": "你是AI助理，回答很简洁"},
        {"role": "user", "content": "小明有两条宠物狗"},
        {"role": "assistant", "content": "OK"},
        {"role": "user", "content": "小红有3只宠物猫"},
        {"role": "assistant", "content": "好的"},
        {"role": "user", "content": "总共有几只宠物，几种？"},
    ],
    stream = True
)

for chunk in responses:
    print(chunk.choices[0].delta.content, end="", flush=True)