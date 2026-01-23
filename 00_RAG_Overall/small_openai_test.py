from humanfriendly.terminal import message
from openai import OpenAI
client = OpenAI()

def test_simple():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "user", "content": "Explain RAG in 3 bullet points"},
        ],
    )

    print(response.output_text)

# 启用流式处理
def test_stream():
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "你是一名具有丰富经验的AI架构师，精通RAG，Agent，LLM等前沿领域"
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ],
        stream=True #启用流式处理
    )
    # print(completion.choices[0].message.content)
    for chunk in completion:
        print(chunk.choices[0].delta.content, end="")

#启用温度参数
def test_temperture():
    for t in [0, 0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 1.9, 2.0]:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                # {
                #     "role": "system",
                #     "content": "你是一名具有丰富经验的AI架构师，精通RAG，Agent，LLM等前沿领域"
                # },
                {
                    "role": "user",
                    "content": "你是谁？"
                }
            ],
            temperature=t, #温度参数取值在[0,2]，默认为1，越接近于0，多次回答的结果越重复，越接近2，越自由
        )
        print(completion.choices[0].message.content)

#多轮对话
# 初始化消息列表
def test_multi_chat():
    messages = [
        {"role": "user", "content": "1+1等于多少？"}
    ]

    # 第一轮对话
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    response1 = completion.choices[0].message.content
    print("用户: 1+1等于多少？")
    print(f"助手: {response1}\n")

    # 将助手的回复添加到消息历史
    messages.append({"role": "assistant", "content": response1})

    # 第二轮对话（包含之前的上下文）
    messages.append({"role": "user", "content": "再加一呢？"})

    print("messages:{}".format(messages))

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    response2 = completion.choices[0].message.content
    print("用户: 再加一呢？")
    print(f"助手: {response2}")

if __name__ == "__main__":
    # test_simple()
    # test_stream()
    # test_temperture()
    test_multi_chat()
