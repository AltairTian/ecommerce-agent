import matplotlib.pyplot as plt
from pathlib import Path

from app.tools.metric_tool import (
    get_monthly_gmv,
    get_category_sales_ranking,
    get_state_sales_ranking,
    get_monthly_orders,
    get_payment_type_distribution,
    get_avg_review_score,
)

BASE_DIR = Path(__file__).resolve().parents[2]
CHART_DIR = BASE_DIR / "outputs" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

"""保存图表并返回图片路径"""
def save_chart(filename: str) -> str:

    path = CHART_DIR / filename
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return str(path)

# 1. 月销售额趋势图
def plot_monthly_gmv() -> str:
    df = get_monthly_gmv()

    plt.figure(figsize=(12, 6))
    plt.plot(df["month"], df["gmv"], marker="o")

    plt.title("Monthly GMV Trend")
    plt.xlabel("Month")
    plt.ylabel("GMV")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    return save_chart("monthly_gmv.png")

# 2. 品类销售额排行图
def plot_top_categories(limit: int = 10) -> str:
    df = get_category_sales_ranking(limit=limit)

    plt.figure(figsize=(12, 6))
    plt.barh(df["product_category_name"], df["gmv"])

    plt.title(f"Top {limit} Categories by GMV")
    plt.xlabel("GMV")
    plt.ylabel("Product Category")
    plt.gca().invert_yaxis()

    return save_chart("top_categories.png")

# 3. 州销售额排行图
def plot_top_states(limit: int = 10) -> str:
    df = get_state_sales_ranking(limit=limit)

    plt.figure(figsize=(10, 6))
    plt.bar(df["customer_state"], df["gmv"])

    plt.title(f"Top {limit} States by GMV")
    plt.xlabel("Customer State")
    plt.ylabel("GMV")
    plt.xticks(rotation=45)

    return save_chart("top_states.png")


# 4. 月订单趋势图
def plot_monthly_orders() -> str:
    df = get_monthly_orders()

    plt.figure(figsize=(12, 6))
    plt.plot(df["month"], df["order_count"], marker="o")

    plt.title("Monthly Order Trend")
    plt.xlabel("Month")
    plt.ylabel("Order Count")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)

    return save_chart("monthly_orders.png")


# 5. 支付方式分布图
def plot_payment_type_distribution() -> str:
    df = get_payment_type_distribution()

    plt.figure(figsize=(8, 6))
    plt.bar(df["payment_type"], df["row_count"])

    plt.title("Payment Type Distribution")
    plt.xlabel("Payment Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)

    return save_chart("payment_type_distribution.png")


# 6. 支付金额分布图
def plot_payment_value_distribution() -> str:
    df = get_payment_type_distribution()

    plt.figure(figsize=(8, 6))
    plt.bar(df["payment_type"], df["total_payment_value"])

    plt.title("Payment Value by Payment Type")
    plt.xlabel("Payment Type")
    plt.ylabel("Total Payment Value")
    plt.xticks(rotation=45)

    return save_chart("payment_value_distribution.png")





# 7. 一次性生成所有图表
def generate_all_charts() -> dict:
    data_charts = {
        "monthly_gmv": plot_monthly_gmv(),
        "top_categories": plot_top_categories(),
        "top_states": plot_top_states(),
        "monthly_orders": plot_monthly_orders(),
        "payment_type_distribution": plot_payment_type_distribution(),
        "payment_value_distribution": plot_payment_value_distribution(),

    }

    return data_charts


if __name__ == "__main__":
    charts = generate_all_charts()

    for name, path in charts.items():
        print(f"{name}: {path}")