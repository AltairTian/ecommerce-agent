"""Streamlit 前端 —— 电商数据分析 Agent 的唯一 UI 入口。

运行方式：
    streamlit run ui/streamlit_app.py
"""

import sys
from pathlib import Path

# 确保项目根目录在 Python path 中
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from src.agent import run_agent
from src.tools.charts import (
    plot_monthly_gmv,
    plot_top_categories,
    plot_top_states,
    plot_monthly_orders,
    plot_payment_type_distribution,
    plot_payment_value_distribution,
)

st.set_page_config(
    page_title="电商数据分析 Agent",
    page_icon="📊",
    layout="wide",
)

st.title("电商数据分析 Agent")
st.write("基于 LangChain + Ollama + SQLite 的本地电商数据分析助手")

# ── 侧边栏：图表功能 ──────────────────────────────

st.sidebar.title("图表分析")

CHART_OPTIONS = {
    "月GMV趋势图": plot_monthly_gmv,
    "品类销售额排行图": plot_top_categories,
    "州销售额排行图": plot_top_states,
    "月订单趋势图": plot_monthly_orders,
    "支付方式分布图": plot_payment_type_distribution,
    "支付金额分布图": plot_payment_value_distribution,
}

selected_chart = st.sidebar.selectbox("选择要生成的图表", list(CHART_OPTIONS.keys()))

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

st.subheader("自然语言数据分析")

question = st.text_input(
    "请输入你的分析问题",
    placeholder="例如：当前总GMV是多少？请生成一份完整经营分析报告。",
)

col1, col2 = st.columns([1, 5])

with col1:
    submit = st.button("提交问题")
with col2:
    clear = st.button("清空结果")

if clear:
    st.session_state.pop("agent_answer", None)
    st.session_state.pop("chart_path", None)
    st.session_state.pop("chart_name", None)

if submit:
    if not question.strip():
        st.warning("请输入问题后再提交。")
    else:
        with st.spinner("Agent 正在分析中..."):
            try:
                answer = run_agent(question)
                st.session_state["agent_answer"] = answer
            except Exception as e:
                st.error("Agent 调用失败")
                st.exception(e)

# ── 显示结果 ─────────────────────────────────────

if "agent_answer" in st.session_state:
    st.subheader("Agent 分析结果")
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
st.subheader("可尝试的问题")

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
    "请生成一份完整的电商经营分析报告。",
]

for example in EXAMPLES:
    st.code(example)
