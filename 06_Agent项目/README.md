# 06_Agent项目 — 扫地机器人智能客服 Agent

基于 LangChain ReAct Agent 的扫地/扫拖一体机器人智能客服系统，具备知识库检索、天气查询、用户定位、个性化报告生成等多工具协同能力，使用 Streamlit 作为 Web 界面。

## 目录结构

```text
06_Agent项目/
├── app.py                        # Streamlit Web 入口（待开发）
├── agent/
│   ├── tools/
│   │   ├── agent_tools.py        # Agent 工具定义（待开发）
│   │   └── middleware.py         # 中间件（待开发）
│   └── react_agent.py           # ReactAgent 核心类（待开发）
├── rag/
│   ├── rag_service.py            # RAG 检索+总结服务（待开发）
│   └── vector_store.py           # 向量存储服务（待开发）
├── model/
│   └── factory.py                # 模型工厂（ChatOllama + HuggingFace Embedding）
├── config/
│   ├── rag.yaml                  # 模型配置（chat_model, embedding_model）
│   ├── chroma.yaml               # ChromaDB 配置（collection, chunk, 文件类型）
│   ├── prompts.yaml              # 提示词文件路径映射
│   └── agent.yaml                # Agent 配置（外部数据路径）
├── prompts/
│   ├── main_prompt.txt           # 主系统提示词（ReAct + 7 工具定义）
│   ├── rag_summarize.txt         # RAG 总结提示词
│   └── report_prompt.txt         # 报告生成提示词
├── data/
│   ├── 扫地机器人100问.pdf
│   ├── 扫地机器人100问2.txt
│   ├── 扫拖一体机器人100问.txt
│   ├── 故障排除.txt
│   ├── 维护保养.txt
│   ├── 选购指南.txt
│   └── external/
│       └── records.csv           # 用户使用记录（报告数据源）
├── utils/
│   ├── __init__.py               # 包标识
│   ├── path_tools.py             # 路径工具（项目根目录解析）
│   ├── config_handler.py         # YAML 配置加载器
│   ├── file_handler.py           # 文件处理（MD5、文档加载器）
│   ├── logger_handler.py         # 日志工具（控制台 + 文件双输出）
│   └── prompt_loader.py          # 提示词加载器
└── logs/                         # 日志输出目录（运行后生成）
```

## 架构图

```mermaid
graph TB
    subgraph UI["Web 层"]
        APP["app.py<br/>Streamlit 界面"]
    end

    subgraph Agent["Agent 核心"]
        RA["ReactAgent<br/>react_agent.py"]
        MW["Middleware<br/>middleware.py"]
    end

    subgraph Tools["工具层 tools/"]
        T1["rag_summarize<br/>知识库检索总结"]
        T2["get_weather<br/>天气查询"]
        T3["get_user_location<br/>用户定位"]
        T4["get_user_id<br/>获取用户 ID"]
        T5["get_current_month<br/>获取当前月份"]
        T6["fetch_external_data<br/>查询用户使用记录"]
        T7["fill_context_for_report<br/>报告上下文注入"]
    end

    subgraph RAG["RAG 服务层"]
        RS["RagSummarizeService<br/>rag_service.py"]
        VSS["VectorStoreService<br/>vector_store.py"]
    end

    subgraph Model["模型层"]
        CM["ChatOllama<br/>qwen2.5:14b"]
        EM["HuggingFaceEmbeddings<br/>bge-small-zh-v1.5"]
        MF["ModelFactory<br/>factory.py"]
    end

    subgraph Storage["存储层"]
        CD["ChromaDB<br/>向量库"]
        CSV["records.csv<br/>用户使用记录"]
        KB["知识库文档<br/>data/*.txt, *.pdf"]
    end

    subgraph Infra["基础设施 utils/"]
        CFG["config_handler<br/>配置加载"]
        LOG["logger_handler<br/>日志"]
        FHU["file_handler<br/>文件处理"]
        PT["path_tools<br/>路径工具"]
        PL["prompt_loader<br/>提示词加载"]
    end

    APP -->|用户提问| RA
    RA -->|ReAct 循环| MW
    MW -->|monitor_tool| Tools
    MW -->|log_before_model| CM
    MW -->|report_prompt_switch| PL

    T1 --> RS
    RS --> VSS
    VSS --> CD
    VSS --> EM
    RS --> CM
    T6 --> CSV

    MF --> CM
    MF --> EM

    KB -->|离线入库| VSS

    CFG -.-> MF
    CFG -.-> RS
    CFG -.-> VSS
    LOG -.-> RA
    PL -.-> RA
```

## 数据流

### 离线流程（知识库构建）

```mermaid
sequenceDiagram
    participant KB as 知识库文档 (data/)
    participant FH as file_handler
    participant VSS as VectorStoreService
    participant Split as 文本分割器
    participant Emb as Embedding 模型
    participant DB as ChromaDB

    KB->>FH: 扫描 txt/pdf/csv 文件
    FH->>FH: MD5 校验（跳过已入库文件）
    FH->>VSS: load_document()
    VSS->>Split: 分割文档 (chunk_size=200)
    Split-->>VSS: 文档块列表
    VSS->>Emb: 向量化
    Emb-->>DB: 存入向量库
```

### 在线流程（问答 / 报告生成）

```mermaid
sequenceDiagram
    participant U as 用户
    participant APP as Streamlit
    participant RA as ReactAgent
    participant MW as Middleware
    participant T as Tools
    participant RAG as RagSummarizeService
    participant DB as ChromaDB
    participant LLM as ChatOllama

    U->>APP: 输入问题
    APP->>RA: execute_stream(input)

    loop ReAct 循环（最多 5 次工具调用）
        RA->>LLM: 思考：分析需要哪个工具
        LLM-->>RA: Action: 工具名 + 参数
        RA->>MW: monitor_tool / log_before_model
        MW->>T: 调用对应工具

        alt rag_summarize（知识检索）
            T->>RAG: query 检索词
            RAG->>DB: 向量相似度检索 (top-k=3)
            DB-->>RAG: 相关文档
            RAG->>LLM: 基于文档总结
            LLM-->>T: 总结结果
        else get_weather / get_user_location
            T-->>T: 调用外部 API
        else fetch_external_data（报告数据）
            T->>T: 查询 records.csv
        else fill_context_for_report
            T->>MW: report_prompt_switch 切换提示词
        end

        T-->>RA: Observation: 工具返回结果
        RA->>LLM: 再次思考：信息是否充分
    end

    RA->>LLM: 生成最终回答
    LLM-->>RA: 流式输出
    RA-->>APP: 流式返回
    APP-->>U: 逐字显示
```

## 启动

### 前置要求

- Python 3.10+
- Ollama 已安装并运行，且已拉取 `qwen2.5:14b` 模型
- HuggingFace Embedding 模型 `BAAI/bge-small-zh-v1.5`（首次运行自动下载）

### 安装依赖

```bash
pip install langchain langchain-ollama langchain-chroma langchain-huggingface \
            langchain-community streamlit pyyaml pypdf
```

### 1. 构建知识库（首次运行）

```bash
cd 06_Agent项目
python -m rag.vector_store
```

将 `data/` 下的文档向量化入库。

### 2. 启动 Web 应用

```bash
cd 06_Agent项目
streamlit run app.py
```

浏览器访问 `http://localhost:8501` 开始与扫地机器人智能客服对话。
