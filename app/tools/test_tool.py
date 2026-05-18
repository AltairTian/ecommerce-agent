from app.tools.metric_tool import (
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

from app.tools.report_tool import (
    generate_daily_report,
    generate_sales_report,
    generate_delivery_report,
    generate_category_report,
    generate_full_report,
)


def test_metric_function(name, func):
    print(f"\n========== 测试 {name} ==========")

    try:
        result = func()
        print(result)

        if result is None:
            print(f"❌ {name} 返回 None")
        elif result.empty:
            print(f"⚠️ {name} 查询结果为空")
        else:
            print(f"✅ {name} 测试通过")

    except Exception as e:
        print(f"❌ {name} 测试失败")
        print(type(e).__name__)
        print(e)


def test_report_function(name, func):
    print(f"\n========== 测试 {name} ==========")

    try:
        result = func()
        print(result[:1000])

        if not result:
            print(f"❌ {name} 返回空内容")
        else:
            print(f"✅ {name} 测试通过")

    except Exception as e:
        print(f"❌ {name} 测试失败")
        print(type(e).__name__)
        print(e)


if __name__ == "__main__":
    print("\n开始测试 metric_tool.py")

    metric_tests = [
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

    for name, func in metric_tests:
        test_metric_function(name, func)

    print("\n\n开始测试 report_tool.py")

    report_tests = [
        ("generate_daily_report", generate_daily_report),
        ("generate_sales_report", generate_sales_report),
        ("generate_delivery_report", generate_delivery_report),
        ("generate_category_report", generate_category_report),
        ("generate_full_report", generate_full_report),
    ]

    for name, func in report_tests:
        test_report_function(name, func)

    print("\n========== 所有测试执行完毕 ==========")