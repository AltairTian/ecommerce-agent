"""纯 SQL 查询函数 —— 每个函数返回 pd.DataFrame，不包含任何 LangChain 依赖。"""

import pandas as pd
from db.connection import query_db


def get_total_orders() -> pd.DataFrame:
    sql = """
    SELECT COUNT(DISTINCT order_id) AS total_orders
    FROM order_analysis_view
    WHERE order_status = 'delivered';
    """
    return query_db(sql)


def get_total_gmv() -> pd.DataFrame:
    sql = """
    SELECT ROUND(SUM(price + freight_value), 2) AS total_gmv
    FROM order_analysis_view
    WHERE order_status = 'delivered';
    """
    return query_db(sql)


def get_avg_order_value() -> pd.DataFrame:
    sql = """
    SELECT ROUND(
        SUM(price + freight_value) / COUNT(DISTINCT order_id), 2
    ) AS avg_order_value
    FROM order_analysis_view
    WHERE order_status = 'delivered';
    """
    return query_db(sql)


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


def get_avg_review_score() -> pd.DataFrame:
    sql = """
    SELECT ROUND(AVG(review_score), 2) AS avg_review_score
    FROM order_analysis_view
    WHERE order_status = 'delivered' AND review_score IS NOT NULL;
    """
    return query_db(sql)


def get_avg_delivery_days() -> pd.DataFrame:
    sql = """
    SELECT ROUND(
        AVG(
            julianday(order_delivered_customer_date)
            - julianday(order_purchase_timestamp)
        ), 2
    ) AS avg_delivery_days
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_purchase_timestamp IS NOT NULL;
    """
    return query_db(sql)


def get_late_delivery_rate() -> pd.DataFrame:
    sql = """
    SELECT ROUND(
        100.0 * SUM(
            CASE WHEN order_delivered_customer_date > order_estimated_delivery_date
            THEN 1 ELSE 0 END
        ) / COUNT(*), 2
    ) AS late_delivery_rate
    FROM order_analysis_view
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL;
    """
    return query_db(sql)


def get_payment_type_distribution() -> pd.DataFrame:
    sql = """
    SELECT
        payment_type,
        COUNT(*) AS row_count,
        ROUND(SUM(payment_value), 2) AS total_payment_value
    FROM order_analysis_view
    WHERE order_status = 'delivered' AND payment_type IS NOT NULL
    GROUP BY payment_type
    ORDER BY row_count DESC;
    """
    return query_db(sql)


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


def get_canceled_order_count() -> pd.DataFrame:
    sql = """
    SELECT COUNT(DISTINCT order_id) AS canceled_order_count
    FROM order_analysis_view
    WHERE order_status = 'canceled';
    """
    return query_db(sql)


def get_canceled_order_rate() -> pd.DataFrame:
    sql = """
    SELECT ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN order_status = 'canceled' THEN order_id END)
        / COUNT(DISTINCT order_id), 2
    ) AS canceled_order_rate
    FROM order_analysis_view
    WHERE order_status IS NOT NULL;
    """
    return query_db(sql)


def get_total_customers() -> pd.DataFrame:
    sql = """
    SELECT COUNT(DISTINCT customer_unique_id) AS total_customers
    FROM order_analysis_view
    WHERE customer_unique_id IS NOT NULL;
    """
    return query_db(sql)


def get_repeat_customer_rate() -> pd.DataFrame:
    sql = """
    WITH customer_orders AS (
        SELECT
            customer_unique_id,
            COUNT(DISTINCT order_id) AS order_count
        FROM order_analysis_view
        WHERE customer_unique_id IS NOT NULL AND order_status = 'delivered'
        GROUP BY customer_unique_id
    )
    SELECT ROUND(
        100.0 * SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS repeat_customer_rate
    FROM customer_orders;
    """
    return query_db(sql)


def get_top_customers_by_gmv(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        customer_unique_id,
        ROUND(SUM(price + freight_value), 2) AS gmv,
        COUNT(DISTINCT order_id) AS order_count
    FROM order_analysis_view
    WHERE order_status = 'delivered' AND customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
    ORDER BY gmv DESC
    LIMIT {limit};
    """
    return query_db(sql)


def get_customer_state_distribution() -> pd.DataFrame:
    sql = """
    SELECT
        customer_state,
        COUNT(DISTINCT customer_unique_id) AS customer_count
    FROM order_analysis_view
    WHERE customer_state IS NOT NULL AND customer_unique_id IS NOT NULL
    GROUP BY customer_state
    ORDER BY customer_count DESC;
    """
    return query_db(sql)


def get_top_products_by_gmv(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        product_id,
        product_category_name,
        ROUND(SUM(price + freight_value), 2) AS gmv,
        COUNT(DISTINCT order_id) AS order_count
    FROM order_analysis_view
    WHERE order_status = 'delivered' AND product_id IS NOT NULL
    GROUP BY product_id, product_category_name
    ORDER BY gmv DESC
    LIMIT {limit};
    """
    return query_db(sql)


def get_top_products_by_orders(limit: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        product_id,
        product_category_name,
        COUNT(DISTINCT order_id) AS order_count,
        ROUND(SUM(price + freight_value), 2) AS gmv
    FROM order_analysis_view
    WHERE order_status = 'delivered' AND product_id IS NOT NULL
    GROUP BY product_id, product_category_name
    ORDER BY order_count DESC
    LIMIT {limit};
    """
    return query_db(sql)


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
