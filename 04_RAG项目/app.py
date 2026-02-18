import time

import streamlit as st
from rag import RagService
import config_data as config

# 启动：streamlit run app.py

# 标题
st.title("智能客服")
st.divider()  # 分隔符

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助您？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

#  在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:
    # 在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    with st.spinner("bot思考中..."):
        time.sleep(1)
        # 非流式输出
        # answer = st.session_state["rag"].chain.invoke({"input": prompt}, config.session_config)
        # st.chat_message("assistant").write(answer)
        # st.session_state["message"].append({"role": "assistant", "content": answer})

        # 流式输出
        ai_res_list = []
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        stream_res = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        st.chat_message("assistant").write_stream(capture(stream_res, ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})