import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


cursor.execute("""
DROP VIEW IF EXISTS order_analysis_view;
""")


cursor.execute("""
CREATE VIEW order_analysis_view AS

SELECT

    -- 订单信息
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

 -- 时间分析字段
    strftime('%Y-%m', o.order_purchase_timestamp) AS purchase_month,
    julianday(o.order_delivered_customer_date) 
        - julianday(o.order_purchase_timestamp) AS delivery_days,
    julianday(o.order_delivered_customer_date) 
        - julianday(o.order_estimated_delivery_date) AS delay_days,
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1
        ELSE 0
    END AS is_late,

    -- 用户信息
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    -- 商品信息
    oi.product_id,
    p.product_category_name,

    -- 金额信息
    oi.price,
    oi.freight_value,

    -- 支付信息
    pay.payment_type,
    pay.payment_installments,
    pay.payment_value,

    -- 评价信息
    r.review_score,

    -- 卖家
    oi.seller_id

FROM orders o

LEFT JOIN customers c
    ON o.customer_id = c.customer_id

LEFT JOIN order_items oi
    ON o.order_id = oi.order_id

LEFT JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN order_payments pay
    ON o.order_id = pay.order_id

LEFT JOIN order_reviews r
    ON o.order_id = r.order_id


""")



conn.commit()

print("宽表 order_analysis_view 创建成功")

conn.close()