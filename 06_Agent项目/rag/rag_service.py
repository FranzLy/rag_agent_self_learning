from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from torch.ao.quantization.backend_config.executorch import executorch_weight_only_quint8_dtype_config

from model import chat_model
from rag.vector_store import VectorStoreService
from utils import get_abs_path, prompts_config, logger


class RagSummarizeService:
    # 类变量缓存，所有实例共用
    _PROMPT_TEXT: str = None

    def __init__(self, vector_store: VectorStoreService):
        self.vector_store = vector_store
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = self._load_prompt_text()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def _load_prompt_text(self):
        if self._PROMPT_TEXT is not None:
            # 避免重复创建对象的重复读文件加载，从缓存读取
            return self._PROMPT_TEXT

        path = get_abs_path(prompts_config["rag_summarize_prompt_path"])
        try:
            with open(path, "r", encoding="utf-8") as f:
                prompt_text = f.read().strip()
        except FileNotFoundError:
            logger.error(f"不存在该系统提示词文件：{path}")
            raise FileNotFoundError(f"不存在该系统提示词文件：{path}")
        except PermissionError:
            logger.error(f"无权限读取提示词文件：{path}")
            raise PermissionError(f"无权限读取提示词文件：{path}")
        except UnicodeDecodeError:
            logger.error(f"提示词文件编码错误（需要UTF-8）：{path}")
            raise PermissionError(f"提示词文件编码错误（需要UTF-8）：{path}")
        except Exception as e:
            logger.error(f"读取提示词文件失败：{str(e)}")
            raise RuntimeError(f"读取提示词文件失败：{str(e)}")

        if not prompt_text:
            logger.error(f"提示词文件内容为空：{path}")
            raise ValueError(f"提示词文件内容为空：{path}")

        #     记录缓存
        self._PROMPT_TEXT = prompt_text
        return prompt_text

    def retrieve_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        input_dict = {}

        context_docs = self.retrieve_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"[参考资料{counter}]： 参考资料： {doc.page_content} | 参考元数据： {doc.metadata}\n"
        input_dict["context"] = context
        input_dict["input"] = query

        return self.chain.invoke(input_dict)

if __name__ == '__main__':
    vs = VectorStoreService()
    rag = RagSummarizeService(vs)

    print(rag.rag_summarize("小户型适合哪种扫地机器人？"))