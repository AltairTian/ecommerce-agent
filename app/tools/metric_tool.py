import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "ecommerce.db"

# 执行SQL查询并返回DataFrame
def query_db(sql:str)->pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()
    return df

# 订单总数
def get_total_orders() -> pd.DataFrame:
    sql = """
    SELECT 
        COUNT(DISTINCT order_id) AS total_orders
    FROM order_analysis_view
    WHERE order_status = 'delivered';
    """
    return query_db(sql)

# 总销售额 GMV
def get_total_gmv() -> pd.DataFrame:
    sql = """
    SELECT 
        ROUND(SUM(price + freight_value), 2) AS total_gmv
    FROM order_analysis_view
    WHERE order_status = 'delivered';
    """
    return query_db(sql)

# 平均客单价 AOV
def get_avg_order_value() -> pd.DataFrame:
    sql = """
    SELECT 
        ROUND(
            SUM(price + freight_value) / COUNT(DISTINCT order_id),
            2
        ) AS avg_order_value
    FROM order_analysis_view
    WHERE order_status = 'delivered';
    """
    return query_db(sql)

# 月订单趋势
def get_monthly_orders() -> pd.DataFrame:
    sql = """
    SELECT 
        strftime('%Y-%m', order_purchase_timestamp) AS month,
        COUNT(DISTINCT order_id) AS order_count
    FROM order_analysis_view
    WHERE order_status = 'delivered'
    GROUP BY month
    ORDER BY month;
    """
    return query_db(sql)

# 月销售额趋势
def get_monthly_gmv() -> pd.DataFrame:
    sql = """
    SELECT 
        strftime('%Y-%m', order_purchase_timestamp) AS month,
        ROUND(SUM(price + freight_value), 2) AS gmv
    FROM order_analysis_view
    WHERE order_status = 'delivered'
    GROUP BY month
    ORDER BY month;
    """
    return query_db(sql)


# 品类销售额排行
def get_category_sales_ranking(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT 
        product_category_name,
        ROUND(SUM(price + freight_value), 2) AS gmv
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND product_category_name IS NOT NULL
    GROUP BY product_category_name
    ORDER BY gmv DESC
    LIMIT {limit};
    """
    return query_db(sql)


# 州销售额排行
def get_state_sales_ranking(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT 
        customer_state,
        ROUND(SUM(price + freight_value), 2) AS gmv
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND customer_state IS NOT NULL
    GROUP BY customer_state
    ORDER BY gmv DESC
    LIMIT {limit};
    """
    return query_db(sql)

# 平均评分
def get_avg_review_score() -> pd.DataFrame:
    sql = """
    SELECT 
        ROUND(AVG(review_score), 2) AS avg_review_score
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND review_score IS NOT NULL;
    """
    return query_db(sql)

# 平均配送时长
def get_avg_delivery_days() -> pd.DataFrame:
    sql = """
    SELECT 
        ROUND(
            AVG(
                julianday(order_delivered_customer_date)
                - julianday(order_purchase_timestamp)
            ),
            2
        ) AS avg_delivery_days
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_purchase_timestamp IS NOT NULL;
    """
    return query_db(sql)

# 延迟配送率
def get_late_delivery_rate() -> pd.DataFrame:
    sql = """
    SELECT 
        ROUND(
            100.0 * SUM(
                CASE 
                    WHEN order_delivered_customer_date > order_estimated_delivery_date
                    THEN 1 
                    ELSE 0 
                END
            ) / COUNT(*),
            2
        ) AS late_delivery_rate
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL;
    """
    return query_db(sql)


# 支付方式分布
def get_payment_type_distribution() -> pd.DataFrame:
    sql = """
    SELECT 
        payment_type,
        COUNT(*) AS row_count,
        ROUND(SUM(payment_value), 2) AS total_payment_value
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND payment_type IS NOT NULL
    GROUP BY payment_type
    ORDER BY row_count DESC;
    """
    return query_db(sql)

# ======================
#     订单状态分析
# ======================


# 订单状态分布
def get_order_status_distribution() -> pd.DataFrame:
    sql = """
    SELECT
        order_status,
        COUNT(DISTINCT order_id) AS order_count
    FROM order_analysis_view
    WHERE order_status IS NOT NULL
    GROUP BY order_status
    ORDER BY order_count DESC;
    """
    return query_db(sql)


# 取消订单数量
def get_canceled_order_count() -> pd.DataFrame:
    sql = """
    SELECT
        COUNT(DISTINCT order_id) AS canceled_order_count
    FROM order_analysis_view
    WHERE order_status = 'canceled';
    """
    return query_db(sql)


# 取消订单率
def get_canceled_order_rate() -> pd.DataFrame:
    sql = """
    SELECT
        ROUND(
            100.0 * COUNT(DISTINCT CASE WHEN order_status = 'canceled' THEN order_id END)
            / COUNT(DISTINCT order_id),
            2
        ) AS canceled_order_rate
    FROM order_analysis_view
    WHERE order_status IS NOT NULL;
    """
    return query_db(sql)

# ======================
#      客户分析
# ======================

# 总客户数
def get_total_customers() -> pd.DataFrame:
    sql = """
    SELECT
        COUNT(DISTINCT customer_unique_id) AS total_customers
    FROM order_analysis_view
    WHERE customer_unique_id IS NOT NULL;
    """
    return query_db(sql)


# 复购客户率
def get_repeat_customer_rate() -> pd.DataFrame:
    sql = """
    WITH customer_orders AS (
        SELECT
            customer_unique_id,
            COUNT(DISTINCT order_id) AS order_count
        FROM order_analysis_view
        WHERE customer_unique_id IS NOT NULL
          AND order_status = 'delivered'
        GROUP BY customer_unique_id
    )
    SELECT
        ROUND(
            100.0 * SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END)
            / COUNT(*),
            2
        ) AS repeat_customer_rate
    FROM customer_orders;
    """
    return query_db(sql)


# GMV最高客户排行
def get_top_customers_by_gmv(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        customer_unique_id,
        ROUND(SUM(price + freight_value), 2) AS gmv,
        COUNT(DISTINCT order_id) AS order_count
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
    ORDER BY gmv DESC
    LIMIT {limit};
    """
    return query_db(sql)


# 客户州分布
def get_customer_state_distribution() -> pd.DataFrame:
    sql = """
    SELECT
        customer_state,
        COUNT(DISTINCT customer_unique_id) AS customer_count
    FROM order_analysis_view
    WHERE customer_state IS NOT NULL
      AND customer_unique_id IS NOT NULL
    GROUP BY customer_state
    ORDER BY customer_count DESC;
    """
    return query_db(sql)

# ======================
#      商品分析
# ======================

# GMV最高商品排行
def get_top_products_by_gmv(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        product_id,
        product_category_name,
        ROUND(SUM(price + freight_value), 2) AS gmv,
        COUNT(DISTINCT order_id) AS order_count
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND product_id IS NOT NULL
    GROUP BY product_id, product_category_name
    ORDER BY gmv DESC
    LIMIT {limit};
    """
    return query_db(sql)


# 订单量最高商品排行
def get_top_products_by_orders(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        product_id,
        product_category_name,
        COUNT(DISTINCT order_id) AS order_count,
        ROUND(SUM(price + freight_value), 2) AS gmv
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND product_id IS NOT NULL
    GROUP BY product_id, product_category_name
    ORDER BY order_count DESC
    LIMIT {limit};
    """
    return query_db(sql)


# 低评分品类
def get_low_review_categories(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        product_category_name,
        ROUND(AVG(review_score), 2) AS avg_review_score,
        COUNT(DISTINCT order_id) AS order_count,
        ROUND(SUM(price + freight_value), 2) AS gmv
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND product_category_name IS NOT NULL
      AND review_score IS NOT NULL
    GROUP BY product_category_name
    HAVING COUNT(DISTINCT order_id) >= 10
    ORDER BY avg_review_score ASC
    LIMIT {limit};
    """
    return query_db(sql)

if __name__ == "__main__":
    print("订单总数：")
    print(get_total_orders())

    print("\n总销售额 GMV：")
    print(get_total_gmv())

    print("\n平均客单价 AOV：")
    print(get_avg_order_value())

    print("\n月订单趋势：")
    print(get_monthly_orders().head())

    print("\n月销售额趋势：")
    print(get_monthly_gmv().head())

    print("\n品类销售额排行：")
    print(get_category_sales_ranking())

    print("\n州销售额排行：")
    print(get_state_sales_ranking())

    print("\n平均评分：")
    print(get_avg_review_score())

    print("\n平均配送时长：")
    print(get_avg_delivery_days())

    print("\n延迟配送率：")
    print(get_late_delivery_rate())

    print("\n支付方式分布：")
    print(get_payment_type_distribution())