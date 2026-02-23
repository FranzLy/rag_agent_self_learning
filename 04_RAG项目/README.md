# 04_RAG项目 — 智能客服 RAG 系统

基于 LangChain + ChromaDB + Ollama 的检索增强生成（RAG）智能客服系统，提供知识库上传和智能问答两大功能，使用 Streamlit 作为 Web 界面。

## 目录结构

```text
04_RAG项目/
├── app.py                  # 智能客服问答 Web 应用（Streamlit）
├── app_file_uploader.py    # 知识库文件上传 Web 应用（Streamlit）
├── rag.py                  # RAG 核心服务，构建检索-生成链
├── vector_stores.py        # 向量存储服务，封装 ChromaDB 检索器
├── knowledge_base.py       # 知识库管理，处理文本入库、MD5 去重
├── chat_history_store.py   # 对话历史持久化（基于文件的消息存储）
├── config_data.py          # 全局配置（模型、分割参数、向量库等）
├── data/                   # 知识库原始数据
│   ├── 尺码推荐.txt
│   ├── 洗涤养护.txt
│   └── 颜色选择.txt
├── chroma_db/              # ChromaDB 持久化存储（运行后生成）
└── user_001/               # 用户会话历史存储（运行后生成）
```

## 架构图

```mermaid
graph TB
    subgraph Web["Streamlit Web 层"]
        A1["app.py<br/>智能客服问答"]
        A2["app_file_uploader.py<br/>知识库上传"]
    end

    subgraph Core["核心服务层"]
        R["RagService<br/>rag.py"]
        KB["KnowledgeBaseService<br/>knowledge_base.py"]
    end

    subgraph Storage["存储层"]
        VS["VectorStoreService<br/>vector_stores.py"]
        CH["FileChatMessageHistory<br/>chat_history_store.py"]
        CD["ChromaDB<br/>chroma_db/"]
        FH["会话文件<br/>user_001/"]
    end

    subgraph Model["模型层"]
        LLM["ChatOllama<br/>qwen2.5:14b"]
        EMB["HuggingFaceEmbeddings<br/>bge-small-zh-v1.5"]
    end

    subgraph Config["配置"]
        CFG["config_data.py"]
    end

    A1 -->|用户提问| R
    A2 -->|上传文件| KB
    R --> VS
    R --> CH
    R --> LLM
    KB --> CD
    KB -->|MD5 去重| KB
    VS --> CD
    VS --> EMB
    KB --> EMB
    CH --> FH
    CFG -.->|配置参数| R
    CFG -.->|配置参数| VS
    CFG -.->|配置参数| KB
```

## 数据流

### 离线流程（知识库上传）

```mermaid
sequenceDiagram
    participant U as 用户
    participant Web as app_file_uploader.py
    participant KB as KnowledgeBaseService
    participant MD5 as MD5 去重
    participant Split as 文本分割器
    participant Emb as Embedding 模型
    participant DB as ChromaDB

    U->>Web: 上传 txt 文件
    Web->>KB: upload_by_str(text, filename)
    KB->>MD5: 计算文本 MD5
    MD5-->>KB: MD5 值
    KB->>MD5: check_md5() 是否已存在
    alt 已存在
        KB-->>Web: 跳过，内容已在知识库中
    else 未存在
        KB->>Split: split_text() 分割文本
        Split-->>KB: 文本块列表
        KB->>Emb: 文本向量化
        Emb-->>DB: 存入向量库
        KB->>MD5: save_md5() 记录 MD5
        KB-->>Web: 上传成功
    end
    Web-->>U: 显示结果
```

### 在线流程（智能问答）

```mermaid
sequenceDiagram
    participant U as 用户
    participant Web as app.py
    participant Rag as RagService
    participant Ret as 向量检索器
    participant DB as ChromaDB
    participant Hist as 对话历史
    participant LLM as ChatOllama

    U->>Web: 输入问题
    Web->>Rag: chain.stream(input)
    Rag->>Ret: 提取 input 作为检索词
    Ret->>DB: 相似度检索 (top-k=2)
    DB-->>Ret: 相关文档片段
    Ret-->>Rag: 格式化为 context
    Rag->>Hist: 获取 session 历史
    Hist-->>Rag: history
    Rag->>LLM: prompt(context + history + input)
    LLM-->>Rag: 流式生成回答
    Rag-->>Web: 流式输出
    Web-->>U: 逐字显示回答
```

## 启动

### 前置要求

- Python 3.10+
- Ollama 已安装并运行，且已拉取 `qwen2.5:14b` 模型
- HuggingFace Embedding 模型 `BAAI/bge-small-zh-v1.5` 可自动下载

### 安装依赖

```bash
pip install streamlit langchain langchain-ollama langchain-chroma langchain-huggingface
```

### 1. 启动知识库上传服务（先上传知识）

```bash
cd 04_RAG项目
streamlit run app_file_uploader.py
```

上传 `data/` 目录下的 txt 文件到向量库。

### 2. 启动智能客服问答

```bash
cd 04_RAG项目
streamlit run app.py
```

浏览器访问 `http://localhost:8501` 即可开始对话。
