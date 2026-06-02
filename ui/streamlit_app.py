"""Streamlit 前端 —— 电商数据分析 Agent 的 UI 入口。

支持两种运行模式：
- API 模式：通过 FastAPI 后端调用（推荐，支持 RAG）
- 本地模式：直接调用本地 Agent（无需启动 API 服务）

运行方式：
    streamlit run ui/streamlit_app.py
"""

import sys
from pathlib import Path

# 确保项目根目录在 Python path 中
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import requests

# ── 页面配置 ────────────────────────────────────────

st.set_page_config(
    page_title="电商数据分析 Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 电商数据分析 Agent")
st.write("基于 LangChain + Ollama 的电商数据分析助手 | FastAPI + RAG 增强")

# ── 侧边栏：配置 ────────────────────────────────────

st.sidebar.title("⚙️ 设置")

# 运行模式
mode = st.sidebar.radio(
    "运行模式",
    options=["api", "local"],
    format_func=lambda m: "🌐 API 模式（FastAPI 后端）" if m == "api" else "💻 本地模式（直接调用）",
    help="API 模式需要先启动 FastAPI 服务: uvicorn api.main:app --port 8000",
)

# API 地址
if mode == "api":
    api_base = st.sidebar.text_input(
        "API 地址",
        value="http://127.0.0.1:8000",
        help="FastAPI 服务的地址",
    )
    # 检查连接
    try:
        resp = requests.get(f"{api_base}/api/health", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            st.sidebar.success(f"🟢 已连接 (v{data.get('version', '?')})")
        else:
            st.sidebar.warning("🟡 API 返回异常")
    except requests.ConnectionError:
        st.sidebar.error("🔴 无法连接 API，请先启动服务")
    except Exception:
        st.sidebar.error("🔴 连接失败")

    use_rag = st.sidebar.checkbox("启用 RAG 检索增强", value=False)
else:
    use_rag = st.sidebar.checkbox("启用 RAG 检索增强（本地模式）", value=False)

st.sidebar.divider()

# ── 侧边栏：图表 ────────────────────────────────────

st.sidebar.title("📈 图表分析")

from src.tools.charts import (
    plot_monthly_gmv,
    plot_top_categories,
    plot_top_states,
    plot_monthly_orders,
    plot_payment_type_distribution,
    plot_payment_value_distribution,
)

CHART_OPTIONS = {
    "月GMV趋势图": plot_monthly_gmv,
    "品类销售额排行图": plot_top_categories,
    "州销售额排行图": plot_top_states,
    "月订单趋势图": plot_monthly_orders,
    "支付方式分布图": plot_payment_type_distribution,
    "支付金额分布图": plot_payment_value_distribution,
}

selected_chart = st.sidebar.selectbox("选择图表", list(CHART_OPTIONS.keys()))

if st.sidebar.button("生成图表"):
    try:
        chart_path = CHART_OPTIONS[selected_chart]()
        st.sidebar.success("图表生成成功")
        st.session_state["chart_path"] = chart_path
        st.session_state["chart_name"] = selected_chart
    except Exception as e:
        st.sidebar.error("图表生成失败")
        st.sidebar.exception(e)

# ── 主区域：Agent 问答 ─────────────────────────────

st.subheader("💬 自然语言数据分析")

question = st.text_input(
    "请输入你的分析问题",
    placeholder="例如：当前总GMV是多少？哪个品类销售额最高？请生成一份完整经营分析报告。",
)

col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    submit = st.button("🚀 提交问题", type="primary")
with col2:
    clear = st.button("🗑️ 清空结果")

if clear:
    st.session_state.pop("agent_answer", None)
    st.session_state.pop("agent_mode", None)
    st.session_state.pop("chart_path", None)
    st.session_state.pop("chart_name", None)

if submit:
    if not question.strip():
        st.warning("请输入问题后再提交。")
    else:
        with st.spinner("Agent 正在分析中..."):
            try:
                if mode == "api":
                    answer, resp_mode = _call_api(api_base, question, use_rag)
                else:
                    answer, resp_mode = _call_local(question, use_rag)

                st.session_state["agent_answer"] = answer
                st.session_state["agent_mode"] = resp_mode
            except Exception as e:
                st.error("Agent 调用失败")
                st.exception(e)

# ── 显示结果 ─────────────────────────────────────

if "agent_answer" in st.session_state:
    mode_label = st.session_state.get("agent_mode", "")
    if mode_label:
        st.caption(f"模式：{mode_label}")
    st.subheader("📋 分析结果")
    st.write(st.session_state["agent_answer"])

if "chart_path" in st.session_state:
    st.subheader(st.session_state.get("chart_name", "图表结果"))
    chart_path = Path(st.session_state["chart_path"])
    if chart_path.exists():
        st.image(str(chart_path), use_container_width=True)
    else:
        st.warning(f"图表文件不存在：{chart_path}")

# ── 示例问题 ─────────────────────────────────────

st.divider()
st.subheader("💡 可尝试的问题")

EXAMPLES = [
    "当前总GMV是多少？",
    "订单总数是多少？",
    "平均客单价是多少？",
    "哪个品类销售额最高？",
    "哪个州的销售额最高？",
    "平均配送时长是多少？",
    "延迟配送率是多少？",
    "取消订单率是多少？",
    "客户复购率是多少？",
    "什么是GMV？GMV怎么计算？（试试 RAG 模式）",
    "请生成一份完整的电商经营分析报告。",
]

for example in EXAMPLES:
    st.code(example)


# ── 辅助函数 ─────────────────────────────────────

def _call_api(base_url: str, question: str, use_rag: bool) -> tuple[str, str]:
    """通过 FastAPI 调用 Agent。"""
    payload = {"question": question, "use_rag": use_rag}
    resp = requests.post(
        f"{base_url}/api/chat",
        json=payload,
        timeout=120,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"API 返回 {resp.status_code}: {resp.text}")
    data = resp.json()
    return data["answer"], data.get("mode", "api")


def _call_local(question: str, use_rag: bool) -> tuple[str, str]:
    """直接调用本地 Agent（无需 API 服务）。"""
    if use_rag:
        from src.rag.retriever import retrieve_as_context
        rag_context = retrieve_as_context(question, top_k=3)
        if rag_context:
            question = (
                f"【知识库上下文】\n{rag_context}\n\n"
                f"【用户问题】\n{question}"
            )
            mode = "local (rag)"
        else:
            mode = "local (rag, no context)"
    else:
        mode = "local"

    from src.agent.agent import run_agent
    return run_agent(question), mode
