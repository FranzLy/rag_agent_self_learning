from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    def __init__(self, embedding):
        self.embedding = embedding # 传入的嵌入模型
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        """返回向量检索器，方便加入chain"""
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})

if __name__ == "__main__":
    from langchain_huggingface import HuggingFaceEmbeddings
    retriever = VectorStoreService(HuggingFaceEmbeddings(
        model_name=config.embedding_model_name,
    )).get_retriever()

    res = retriever.invoke("我的体重140斤，尺码推荐")
    print(res)

