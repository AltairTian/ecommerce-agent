"""指标查询函数的单元测试。"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.tools.metrics import (
    get_total_orders,
    get_total_gmv,
    get_avg_order_value,
    get_monthly_orders,
    get_monthly_gmv,
    get_category_sales_ranking,
    get_state_sales_ranking,
    get_avg_review_score,
    get_avg_delivery_days,
    get_late_delivery_rate,
    get_payment_type_distribution,
    get_order_status_distribution,
    get_canceled_order_count,
    get_canceled_order_rate,
    get_total_customers,
    get_repeat_customer_rate,
    get_top_customers_by_gmv,
    get_customer_state_distribution,
    get_top_products_by_gmv,
    get_top_products_by_orders,
    get_low_review_categories,
)


def _test_func(name, func):
    try:
        df = func()
        assert df is not None, f"{name} 返回 None"
        assert not df.empty, f"{name} 查询结果为空"
        print(f"PASS {name}")
    except Exception as e:
        print(f"FAIL {name}: {e}")


METRIC_TESTS = [
    ("get_total_orders", get_total_orders),
    ("get_total_gmv", get_total_gmv),
    ("get_avg_order_value", get_avg_order_value),
    ("get_monthly_orders", get_monthly_orders),
    ("get_monthly_gmv", get_monthly_gmv),
    ("get_category_sales_ranking", get_category_sales_ranking),
    ("get_state_sales_ranking", get_state_sales_ranking),
    ("get_avg_review_score", get_avg_review_score),
    ("get_avg_delivery_days", get_avg_delivery_days),
    ("get_late_delivery_rate", get_late_delivery_rate),
    ("get_payment_type_distribution", get_payment_type_distribution),
    ("get_order_status_distribution", get_order_status_distribution),
    ("get_canceled_order_count", get_canceled_order_count),
    ("get_canceled_order_rate", get_canceled_order_rate),
    ("get_total_customers", get_total_customers),
    ("get_repeat_customer_rate", get_repeat_customer_rate),
    ("get_top_customers_by_gmv", get_top_customers_by_gmv),
    ("get_customer_state_distribution", get_customer_state_distribution),
    ("get_top_products_by_gmv", get_top_products_by_gmv),
    ("get_top_products_by_orders", get_top_products_by_orders),
    ("get_low_review_categories", get_low_review_categories),
]


if __name__ == "__main__":
    for name, func in METRIC_TESTS:
        _test_func(name, func)
    print("\n全部指标测试完成。")
