# 报告输出
# 1. 总销售额
# 2. 订单趋势
# 3. TOP品类
# 4. 配送表现
# 5. 用户评价
# 6. AI生成经营建议


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


def _value(df, column_name):
    """
    从单行 DataFrame 中取值，避免重复写 iloc。
    """
    if df.empty:
        return None
    return df.iloc[0][column_name]


# ======================
# 1. 日常经营报告
# ======================

def generate_daily_report() -> str:
    total_orders = _value(get_total_orders(), "total_orders")
    total_gmv = _value(get_total_gmv(), "total_gmv")
    avg_order_value = _value(get_avg_order_value(), "avg_order_value")
    avg_review_score = _value(get_avg_review_score(), "avg_review_score")
    avg_delivery_days = _value(get_avg_delivery_days(), "avg_delivery_days")
    late_delivery_rate = _value(get_late_delivery_rate(), "late_delivery_rate")

    report = f"""
【电商日常经营报告】

一、核心经营指标
- 总订单数：{total_orders}
- 总GMV：{total_gmv}
- 平均客单价：{avg_order_value}

二、用户体验指标
- 平均评分：{avg_review_score}
- 平均配送时长：{avg_delivery_days} 天
- 延迟配送率：{late_delivery_rate}%

三、简要结论
当前业务已具备基础交易规模，可继续从销售趋势、重点品类、区域分布、配送效率和用户评价等角度进行深入分析。
"""
    return report.strip()


# ======================
# 2. 销售分析报告
# ======================

def generate_sales_report() -> str:
    total_gmv = _value(get_total_gmv(), "total_gmv")
    total_orders = _value(get_total_orders(), "total_orders")
    avg_order_value = _value(get_avg_order_value(), "avg_order_value")

    monthly_gmv = get_monthly_gmv()
    monthly_orders = get_monthly_orders()
    top_states = get_state_sales_ranking(limit=5)
    payment_dist = get_payment_type_distribution()

    latest_month_gmv = monthly_gmv.tail(1).to_string(index=False)
    latest_month_orders = monthly_orders.tail(1).to_string(index=False)
    top_states_text = top_states.to_string(index=False)
    payment_text = payment_dist.to_string(index=False)

    report = f"""
【销售分析报告】

一、销售总览
- 总GMV：{total_gmv}
- 总订单数：{total_orders}
- 平均客单价：{avg_order_value}

二、最近月份销售表现
{latest_month_gmv}

三、最近月份订单表现
{latest_month_orders}

四、销售额最高的地区 TOP 5
{top_states_text}

五、支付方式分布
{payment_text}

六、简要结论
销售分析应重点关注 GMV 趋势、订单趋势、地区贡献和支付结构。后续可以结合月份变化进一步判断是否存在季节性波动或重点市场集中现象。
"""
    return report.strip()


# ======================
# 3. 配送分析报告
# ======================

def generate_delivery_report() -> str:
    avg_delivery_days = _value(get_avg_delivery_days(), "avg_delivery_days")
    late_delivery_rate = _value(get_late_delivery_rate(), "late_delivery_rate")
    state_sales = get_state_sales_ranking(limit=10)

    state_text = state_sales.to_string(index=False)

    report = f"""
【配送表现分析报告】

一、配送核心指标
- 平均配送时长：{avg_delivery_days} 天
- 延迟配送率：{late_delivery_rate}%

二、高销售额地区参考
{state_text}

三、简要结论
如果延迟配送率较高，应优先排查高销售额地区的物流压力。后续可以进一步补充“各州平均配送时长”和“各州延迟配送率”，用于定位配送效率较低的区域。
"""
    return report.strip()


# ======================
# 4. 品类分析报告
# ======================

def generate_category_report() -> str:
    top_categories = get_category_sales_ranking(limit=10)
    low_review_categories = get_low_review_categories(limit=10)
    top_products_gmv = get_top_products_by_gmv(limit=10)
    top_products_orders = get_top_products_by_orders(limit=10)

    top_categories_text = top_categories.to_string(index=False)
    low_review_text = low_review_categories.to_string(index=False)
    top_products_gmv_text = top_products_gmv.to_string(index=False)
    top_products_orders_text = top_products_orders.to_string(index=False)

    report = f"""
【品类与商品分析报告】

一、销售额最高品类 TOP 10
{top_categories_text}

二、低评分品类 TOP 10
{low_review_text}

三、GMV最高商品 TOP 10
{top_products_gmv_text}

四、订单量最高商品 TOP 10
{top_products_orders_text}

五、简要结论
品类分析应同时关注销售贡献和用户评价。高GMV品类适合作为重点经营对象；低评分但订单量较高的品类，应重点排查商品质量、物流体验或售后问题。
"""
    return report.strip()


# ======================
# 5. 完整经营分析报告
# ======================

def generate_full_report() -> str:
    daily_report = generate_daily_report()
    sales_report = generate_sales_report()
    delivery_report = generate_delivery_report()
    category_report = generate_category_report()

    order_status = get_order_status_distribution()
    canceled_count = _value(get_canceled_order_count(), "canceled_order_count")
    canceled_rate = _value(get_canceled_order_rate(), "canceled_order_rate")

    total_customers = _value(get_total_customers(), "total_customers")
    repeat_customer_rate = _value(get_repeat_customer_rate(), "repeat_customer_rate")
    top_customers = get_top_customers_by_gmv(limit=10)
    customer_state = get_customer_state_distribution().head(10)

    order_status_text = order_status.to_string(index=False)
    top_customers_text = top_customers.to_string(index=False)
    customer_state_text = customer_state.to_string(index=False)

    report = f"""
{daily_report}

==================================================

{sales_report}

==================================================

{delivery_report}

==================================================

{category_report}

==================================================

【订单状态分析】

一、订单状态分布
{order_status_text}

二、取消订单情况
- 取消订单数：{canceled_count}
- 取消订单率：{canceled_rate}%

简要结论：
取消订单率可以用于判断交易流程、库存管理或用户下单体验是否存在问题。

==================================================

【客户分析】

一、客户核心指标
- 总客户数：{total_customers}
- 复购客户率：{repeat_customer_rate}%

二、GMV最高客户 TOP 10
{top_customers_text}

三、客户数量最高地区 TOP 10
{customer_state_text}

简要结论：
客户分析应重点关注复购率、核心客户贡献和地区分布。如果复购率较低，可以考虑通过优惠券、会员体系、精准推荐等方式提升用户留存。

==================================================

【综合经营建议】

1. 优先关注高GMV品类，保持核心品类供给稳定。
2. 对低评分品类进行质量、物流和售后问题排查。
3. 对高销售额地区加强物流能力和库存配置。
4. 结合订单状态分布，分析取消订单的主要原因。
5. 通过复购率和高价值客户分析，设计用户留存策略。
"""
    return report.strip()


if __name__ == "__main__":
    print(generate_full_report())