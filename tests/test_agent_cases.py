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
from src.agent import run_agent

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
