"""报告函数的单元测试。"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.tools.reports import (
    generate_daily_report,
    generate_sales_report,
    generate_delivery_report,
    generate_category_report,
    generate_full_report,
)


def _test_report(name, func):
    try:
        result = func()
        assert result, f"{name} 返回空内容"
        print(f"PASS {name} (length={len(result)})")
    except Exception as e:
        print(f"FAIL {name}: {e}")


REPORT_TESTS = [
    ("generate_daily_report", generate_daily_report),
    ("generate_sales_report", generate_sales_report),
    ("generate_delivery_report", generate_delivery_report),
    ("generate_category_report", generate_category_report),
    ("generate_full_report", generate_full_report),
]


if __name__ == "__main__":
    for name, func in REPORT_TESTS:
        _test_report(name, func)
    print("\n全部报告测试完成。")
