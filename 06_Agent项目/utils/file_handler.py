import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_core.documents import Document

from .logger_handler import logger


def get_file_md5_hex(file_path: str) -> str:
    """
        计算文件的MD5哈希值，返回十六进制字符串
        :param file_path: 文件的绝对/相对路径
        :return: 成功返回32位MD5十六进制字符串，失败返回None
    """
    # 1. 校验文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"[get_file_md5_hex]文件{file_path}不存在")
        return None

    # 2. 校验是否是文件（避免传入文件夹路径）
    if not os.path.isfile(file_path):
        logger.error(f"[get_file_md5_hex]{file_path}不是文件")
        return None

    # 3. 初始化MD5对象
    md5_obj = hashlib.md5()

    # 4. 分片读取大文件（避免一次性加载占满内存）
    chunk_size = 4096  # 4KB分片，避免文件过大爆内存
    try:
        with open(file_path, 'rb') as f:  # 必须以二进制模式打开
            while chunk := f.read(chunk_size):  # 逐片读取
                md5_obj.update(chunk)  # 更新MD5摘要

            # 5. 获取十六进制字符串（32位小写）
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except PermissionError:
        print(f"[get_file_md5_hex]错误：无权限读取文件 {file_path}")
        return None
    except Exception as e:
        logger.error(f"[get_file_md5_hex]计算文件{file_path}md5失败, {str(e)}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]) -> tuple[str]:
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return tuple(files)

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)


def csv_loader(path: str, source_column=None, encoding='utf-8', csv_args=None) -> list[Document]:
    loader = CSVLoader(
        file_path=path,
        source_column=source_column,
        encoding=encoding,
        csv_args=csv_args
    )

    return loader.load()


def pdf_loader(path: str, password: str = None) -> list[Document]:
    return PyPDFLoader(path, password).load()


def txt_loader(path: str) -> list[Document]:
    return TextLoader(path, encoding="utf-8").load()
