"""
知识库
"""
from datetime import datetime
import hashlib
import os

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data as config
from langchain_chroma import Chroma

def check_md5(md5_str: str):
    """检查传入的md5字符串是否已经被处理过了
        return False(md5未处理过) True(已经处理过，已有记录)
    """

    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip()  # 处理字符串前后的空格和回车
            if line == md5_str:
                return True

        return False


def save_md5(md5_str: str):
    """将传入的md5字符串，记录到文件内保存"""
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    """将传入的字符串转换为md5字符串"""

    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5()  # 得到md5对象
    md5_obj.update(str_bytes)  # 更新内容（传入即将要转换的字节数组）
    md5_hex = md5_obj.hexdigest()  # 得到md5的十六进制字符串

    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        # 确保文件夹存在
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name = config.collection_name, # 数据库表名
            embedding_function= HuggingFaceEmbeddings(
                model_name=config.model_name,
            ),
            persist_directory = config.persist_directory, # 数据库本地存储文件夹
        )  # 向量存储的实例Chroma向量库对象
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )  # 文本分割器对象

    def upload_by_str(self, data: str, filename):
        """将传入的字符串，进行向量化，存入向量数据库中"""
        # 先得到传入字符串的md5值
        md5_hex = get_string_md5(data)

        # 检查md5是否已包含在知识库中
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        # 分割并转化为列表
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.splitter.split_text(data)
        else:
            knowledge_chunks = [data]


        # 利用chroma.add_texts添加文本数据至向量库
        metadata = {
            "source": filename,
            # 2026-02-18 16:20:00
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "franz"
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        # 添加完之后记录md5
        save_md5(md5_hex)

        return "[成功]内容已成功上传至向量库"

if __name__ == '__main__':
    # r1 = get_string_md5("周杰伦")
    # r2 = get_string_md5("周杰伦")
    # r3 = get_string_md5("周杰轮")
    #
    # print(r1)
    # print(r2)
    # print(r3)
    #
    # save_md5(r1)
    # print(check_md5(r1))

    service = KnowledgeBaseService()
    result = service.upload_by_str("周杰伦", "testfile")
    print(result)
