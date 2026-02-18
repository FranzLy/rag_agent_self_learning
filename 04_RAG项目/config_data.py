md5_path = "./md5.text"

collection_name = "rag"
embedding_model_name = "BAAI/bge-small-zh-v1.5"
persist_directory = "./chroma_db"

# splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 1000

# service name
service_name = "KnowledgeBaseService"

# vector store
similarity_threshold = 2

# chat model
chat_model_name = "qwen2.5:14b"

# session config
session_config = {
    "configurable": {
        "session_id": "user_001",
    }
}
