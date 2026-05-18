from langchain.tools import tool

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


def df_to_text(df, max_rows: int = 10) -> str:
    """
    将 DataFrame 转成适合 Agent 返回的文本。
    """
    if df is None:
        return "查询失败，未返回数据。"

    if df.empty:
        return "查询结果为空。"

    return df.head(max_rows).to_string(index=False)


@tool
def total_orders_tool() -> str:
    """查询已完成订单的总订单数。"""
    return df_to_text(get_total_orders())


@tool
def total_gmv_tool() -> str:
    """查询已完成订单的总GMV，也就是总销售额。"""
    return df_to_text(get_total_gmv())


@tool
def avg_order_value_tool() -> str:
    """查询已完成订单的平均客单价AOV。"""
    return df_to_text(get_avg_order_value())


@tool
def monthly_orders_tool() -> str:
    """查询每个月的订单数量趋势。"""
    return df_to_text(get_monthly_orders(), max_rows=50)


@tool
def monthly_gmv_tool() -> str:
    """查询每个月的GMV销售额趋势。"""
    return df_to_text(get_monthly_gmv(), max_rows=50)


@tool
def category_sales_ranking_tool() -> str:
    """查询销售额最高的商品品类排行榜。"""
    return df_to_text(get_category_sales_ranking(limit=10))


@tool
def state_sales_ranking_tool() -> str:
    """查询销售额最高的客户所在州排行榜。"""
    return df_to_text(get_state_sales_ranking(limit=10))


@tool
def avg_review_score_tool() -> str:
    """查询已完成订单的平均用户评分。"""
    return df_to_text(get_avg_review_score())


@tool
def avg_delivery_days_tool() -> str:
    """查询已完成订单的平均配送时长，单位为天。"""
    return df_to_text(get_avg_delivery_days())


@tool
def late_delivery_rate_tool() -> str:
    """查询已完成订单的延迟配送率。"""
    return df_to_text(get_late_delivery_rate())


@tool
def payment_type_distribution_tool() -> str:
    """查询不同支付方式的订单数量和支付金额分布。"""
    return df_to_text(get_payment_type_distribution())


@tool
def order_status_distribution_tool() -> str:
    """查询订单状态分布，包括已完成、取消等状态。"""
    return df_to_text(get_order_status_distribution())


@tool
def canceled_order_count_tool() -> str:
    """查询取消订单数量。"""
    return df_to_text(get_canceled_order_count())


@tool
def canceled_order_rate_tool() -> str:
    """查询取消订单率。"""
    return df_to_text(get_canceled_order_rate())


@tool
def total_customers_tool() -> str:
    """查询总客户数量。"""
    return df_to_text(get_total_customers())


@tool
def repeat_customer_rate_tool() -> str:
    """查询复购客户率。"""
    return df_to_text(get_repeat_customer_rate())


@tool
def top_customers_by_gmv_tool() -> str:
    """查询GMV贡献最高的客户排行榜。"""
    return df_to_text(get_top_customers_by_gmv(limit=10))


@tool
def customer_state_distribution_tool() -> str:
    """查询不同州的客户数量分布。"""
    return df_to_text(get_customer_state_distribution(), max_rows=30)


@tool
def top_products_by_gmv_tool() -> str:
    """查询GMV最高的商品排行榜。"""
    return df_to_text(get_top_products_by_gmv(limit=10))


@tool
def top_products_by_orders_tool() -> str:
    """查询订单量最高的商品排行榜。"""
    return df_to_text(get_top_products_by_orders(limit=10))


@tool
def low_review_categories_tool() -> str:
    """查询平均评分较低的商品品类。"""
    return df_to_text(get_low_review_categories(limit=10))


@tool
def daily_report_tool() -> str:
    """生成电商日常经营报告，包含GMV、订单数、客单价、评分、配送等核心指标。"""
    return generate_daily_report()


@tool
def sales_report_tool() -> str:
    """生成销售分析报告，包含GMV、订单趋势、地区销售排行和支付方式分布。"""
    return generate_sales_report()


@tool
def delivery_report_tool() -> str:
    """生成配送表现分析报告，包含平均配送时长和延迟配送率。"""
    return generate_delivery_report()


@tool
def category_report_tool() -> str:
    """生成品类和商品分析报告，包含品类销售排行、低评分品类和商品排行。"""
    return generate_category_report()


@tool
def full_report_tool() -> str:
    """生成完整电商经营分析报告，包含销售、配送、品类、订单状态和客户分析。"""
    return generate_full_report()


tools = [
    total_orders_tool,
    total_gmv_tool,
    avg_order_value_tool,
    monthly_orders_tool,
    monthly_gmv_tool,
    category_sales_ranking_tool,
    state_sales_ranking_tool,
    avg_review_score_tool,
    avg_delivery_days_tool,
    late_delivery_rate_tool,
    payment_type_distribution_tool,
    order_status_distribution_tool,
    canceled_order_count_tool,
    canceled_order_rate_tool,
    total_customers_tool,
    repeat_customer_rate_tool,
    top_customers_by_gmv_tool,
    customer_state_distribution_tool,
    top_products_by_gmv_tool,
    top_products_by_orders_tool,
    low_review_categories_tool,
    daily_report_tool,
    sales_report_tool,
    delivery_report_tool,
    category_report_tool,
    full_report_tool,
]