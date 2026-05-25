"""创建分析视图 —— 将多表 JOIN 展平为 order_analysis_view 宽表。"""

from db.connection import get_connection

VIEW_SQL = """
DROP VIEW IF EXISTS order_analysis_view;

CREATE VIEW order_analysis_view AS

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    strftime('%Y-%m', o.order_purchase_timestamp) AS purchase_month,
    julianday(o.order_delivered_customer_date)
        - julianday(o.order_purchase_timestamp) AS delivery_days,
    julianday(o.order_delivered_customer_date)
        - julianday(o.order_estimated_delivery_date) AS delay_days,
    CASE
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1
        ELSE 0
    END AS is_late,

    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    oi.product_id,
    p.product_category_name,

    oi.price,
    oi.freight_value,

    pay.payment_type,
    pay.payment_installments,
    pay.payment_value,

    r.review_score,

    oi.seller_id

FROM orders o
LEFT JOIN customers c       ON o.customer_id = c.customer_id
LEFT JOIN order_items oi    ON o.order_id = oi.order_id
LEFT JOIN products p        ON oi.product_id = p.product_id
LEFT JOIN order_payments pay ON o.order_id = pay.order_id
LEFT JOIN order_reviews r   ON o.order_id = r.order_id
"""


def create_views() -> None:
    """创建/重建分析视图。"""
    conn = get_connection()
    try:
        conn.executescript(VIEW_SQL)
    finally:
        conn.close()
