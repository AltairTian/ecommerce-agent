"""Agent 集成测试 —— 覆盖核心业务场景，Trace 记录到 LangSmith。

运行方式：
    python tests/test_agent_cases.py
"""

import sys
import io
from pathlib import Path

# 修复 Windows GBK 终端无法打印 emoji 的问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langsmith import traceable
from src.agent.agent import run_agent

TEST_CASES = [
    {
        "id": "case_01",
        "name": "整体销售表现",
        "query": "请帮我总结当前电商业务的整体销售表现，包括 GMV、订单量、客单价，以及你认为最值得关注的问题。",
    },
    {
        "id": "case_02",
        "name": "月度 GMV 趋势",
        "query": "请分析每个月的 GMV 变化趋势，找出销售高峰和低谷月份，并给出可能的业务解释。",
    },
    {
        "id": "case_03",
        "name": "大额订单贡献分析",
        "query": "当前 GMV 是否主要由少数大额订单贡献？请分析订单金额分布，并找出是否存在极端大额订单。",
    },
    {
        "id": "case_04",
        "name": "销售健康诊断",
        "query": """请对当前电商业务做一次销售健康诊断，内容包括：
1. 总体 GMV 和订单量
2. 月度 GMV 趋势
3. 核心品类表现
4. 核心地区表现
5. 目前最值得关注的 3 个问题
6. 下一步运营建议""",
    },
    {
        "id": "case_05",
        "name": "抗幻觉测试：广告 ROI",
        "query": "请分析本月广告投放 ROI，并判断哪个渠道投放效果最好。",
    },
     {
        "id": "case_06",
        "category": "category_analysis",
        "name": "核心品类表现分析",
        "query": "请分析销售额最高的前 5 个品类，并说明这些品类在 GMV、订单量和客单价上的表现差异。",
    },
    {
        "id": "case_07",
        "category": "customer_experience",
        "name": "低评分品类诊断",
        "query": "请找出评分较低但销售额较高的品类，并分析这些品类是否可能存在客户体验问题。",
    },
    {
        "id": "case_08",
        "category": "region_analysis",
        "name": "地区销售表现分析",
        "query": "请分析不同州的销售表现，找出 GMV 最高的地区，并说明这些地区的订单量和客单价是否也较高。",
    },
    {
        "id": "case_09",
        "category": "delivery_analysis",
        "name": "配送效率分析",
        "query": "请分析当前业务的配送效率，包括平均配送时长、延迟配送率，并判断配送是否可能影响用户体验。",
    },
    {
        "id": "case_10",
        "category": "payment_analysis",
        "name": "支付方式分析",
        "query": "请分析不同支付方式的使用情况，包括订单量、支付金额和占比，并判断哪种支付方式最主要。",
    },
    {
        "id": "case_11",
        "category": "diagnosis",
        "name": "GMV 下滑归因分析",
        "query": "如果某个月 GMV 明显下降，请从订单量、客单价、品类结构、地区表现和配送情况几个角度分析可能原因。",
    },
    {
        "id": "case_12",
        "category": "chart_generation",
        "name": "图表生成测试：GMV 趋势图",
        "query": "请生成月度 GMV 趋势图，并结合图表说明 GMV 的变化趋势。",
    },
    {
        "id": "case_13",
        "category": "chart_generation",
        "name": "图表生成测试：品类排行图",
        "query": "请生成销售额最高的前 10 个品类排行图，并总结头部品类的销售特点。",
    },
    {
        "id": "case_14",
        "category": "report_generation",
        "name": "完整经营分析报告",
        "query": "请生成一份完整的电商经营分析报告，包括销售表现、趋势变化、品类表现、地区表现、配送表现、支付表现、主要问题和运营建议。",
    },
    {
        "id": "case_15",
        "category": "anti_hallucination",
        "name": "抗幻觉测试：用户画像",
        "query": "请分析用户年龄、性别和收入水平对购买行为的影响。",
    },
]


@traceable(name="batch_agent_test")
def run_single_case(case: dict) -> dict:
    print("=" * 80)
    print(f"案例编号：{case['id']}")
    print(f"案例名称：{case['name']}")
    print(f"用户问题：{case['query']}")
    print("-" * 80)

    answer = run_agent(case["query"])

    print("Agent 回答：")
    print(answer)
    print("=" * 80)
    print()

    return {
        "case_id": case["id"],
        "case_name": case["name"],
        "query": case["query"],
        "answer": answer,
    }


if __name__ == "__main__":
    results = []
    for case in TEST_CASES:
        result = run_single_case(case)
        results.append(result)
    print("全部测试完成，请到 LangSmith 查看 Trace。")
