"""
基于Streamlit完成web网页上传服务

pip install streamlit

Streamlit：当WEB页面元素发生变化，则代码重新执行一遍
"""

# streamlit run app_file_uploader.py

import time

import streamlit as st
from knowledge_base import KnowledgeBaseService
import config_data as config

# 添加网页标题
st.title("知识库更新服务")

# file_uploader
upload_file = st.file_uploader(
    "请上传txt文件",
    type=['txt'],
    accept_multiple_files=False,  # False表示近接受一个文件上传
)

# 借助streamlit提供的session_state来存储状态
if config.service_name not in st.session_state:
    st.session_state[config.service_name] = KnowledgeBaseService()

if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024  # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小： {file_size: .2f} KB")

    # get_value -> bytes -> decode('utf-8')
    text = upload_file.getvalue().decode("utf-8")
    # st.write(text)

    with st.spinner("载入知识库中...."):  # 在spinner内的代码执行过程中，会有一个转圈动画
        time.sleep(1)
        result = st.session_state[config.service_name].upload_by_str(text, file_name)
        st.write(f"执行结果：{result}")
