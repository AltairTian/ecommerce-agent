# 电商数据分析 Agent

基于 LangChain + Ollama 的电商数据分析 Agent，支持 FastAPI 接口、Streamlit 前端和 RAG 检索增强，通过自然语言查询核心经营指标、生成图表和业务报告。

## 技术栈

- **Agent 框架**: LangChain + langchain-ollama
- **本地模型**: Ollama (qwen3:8b)
- **API 服务**: FastAPI + Uvicorn
- **前端**: Streamlit
- **RAG 检索**: ChromaDB + Sentence-Transformers
- **数据库**: SQLite (巴西 Olist 电商数据集)
- **可观测性**: LangSmith Trace

## 项目结构

```
├── api/                       # FastAPI 接口层
│   ├── main.py                # 应用入口，路由注册
│   ├── middleware/             # 中间件（CORS、日志等）
│   └── routes/
│       ├── chat.py            # Agent 对话接口
│       ├── health.py          # 健康检查
│       └── reports.py         # 报告查询接口
│
├── config/                    # 统一配置层
│   ├── settings.py            # 所有配置从 .env 读取
│   └── llm.py                 # LLM 唯一创建入口
│
├── db/                        # 数据库层
│   ├── connection.py          # 连接管理与查询
│   ├── views.py               # 分析视图定义
│   └── init_db.py             # CSV → SQLite 初始化
│
├── src/                       # 核心代码
│   ├── agent/                 # Agent 模块
│   │   ├── agent.py           # Agent 唯一入口，run_agent()
│   │   └── prompts.py         # 系统提示词
│   ├── rag/                   # RAG 检索增强模块
│   │   ├── embeddings.py      # 文档向量化
│   │   ├── ingestion.py       # 文档摄入管线
│   │   ├── retriever.py       # 检索器
│   │   ├── vector_store.py    # 向量数据库管理
│   │   └── knowledge_base/    # 知识库文档存储
│   ├── schemas/               # Pydantic 数据模型
│   └── tools/                 # Agent 工具集
│       ├── metrics.py         # 21 个 SQL 查询函数
│       ├── charts.py          # matplotlib 图表生成
│       ├── reports.py         # 结构化文本报告
│       └── langchain_tools.py # @tool 包装，统一导出
│
├── ui/                        # Streamlit 前端
│   └── streamlit_app.py
│
├── tests/                     # 测试
│   ├── test_metrics.py
│   ├── test_reports.py
│   ├── test_agent_cases.py
│   └── test_langsmith.py
│
└── outputs/                   # 输出文件
    ├── charts/                # 图表输出
    └── reports/               # 报告输出
```

## 快速开始

### 1. 环境要求

- Python 3.11+
- [Ollama](https://ollama.com) 已安装并运行
- qwen3:8b 模型已拉取

```bash
ollama pull qwen3:8b
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入你的 LangSmith API Key（可选，用于 Trace 监控）：

```
OLLAMA_MODEL=qwen3:8b
OLLAMA_BASE_URL=http://127.0.0.1:11434
LANGSMITH_API_KEY=your_key_here
LANGSMITH_PROJECT=ecommerce-agent

# FastAPI
API_HOST=127.0.0.1
API_PORT=8000

# RAG
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DB_PATH=./src/rag/vector_db
CHUNK_SIZE=500
RAG_TOP_K=5
```

### 4. 初始化数据库

```bash
python db/init_db.py    # 从 CSV 导入原始数据
python -c "from db.views import create_views; create_views()"   # 创建分析视图
```

### 5. 启动服务

#### 方式一：FastAPI（推荐，支持 API 调用）

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 方式二：Streamlit 前端

```bash
streamlit run ui/streamlit_app.py
```

### 6. 运行测试

```bash
python tests/test_metrics.py          # 指标查询测试
python tests/test_reports.py          # 报告生成测试
python tests/test_agent_cases.py      # Agent 集成测试（需要 Ollama 运行中）
```

## 使用示例

在 Streamlit 界面中输入自然语言问题，例如：

- "当前总 GMV 是多少？"
- "请分析每个月的 GMV 变化趋势"
- "哪个品类销售额最高？"
- "平均配送时长和延迟配送率是多少？"
- "请生成一份完整的电商经营分析报告"

## Agent 能力

| 能力 | 说明 |
|------|------|
| 经营指标查询 | GMV、订单量、客单价、复购率、取消率 |
| 趋势分析 | 月度 GMV/订单量变化趋势 |
| 品类分析 | 品类/商品销售额排行、低评分品类 |
| 地区分析 | 州销售额排行、客户地区分布 |
| 配送分析 | 平均配送时长、延迟配送率 |
| 支付分析 | 支付方式分布、支付金额分布 |
| 图表生成 | GMV 趋势图、品类排行图、支付分布图 |
| 报告生成 | 日经营报告、销售报告、配送报告、完整分析报告 |

## 数据来源

[巴西 Olist 电商数据集](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)，包含约 10 万订单、7.3 万商品、10 万客户。
