"""图表生成 —— 依赖 src.tools.metrics 获取数据，用 matplotlib 生成 PNG。"""

import matplotlib
matplotlib.use("Agg")  # 非交互后端，避免子线程 tkinter 崩溃
import matplotlib.pyplot as plt
from config.settings import CHART_DIR
from src.tools.metrics import (
    get_monthly_gmv,
    get_category_sales_ranking,
    get_state_sales_ranking,
    get_monthly_orders,
    get_payment_type_distribution,
)

CHART_DIR.mkdir(parents=True, exist_ok=True)


def _save(filename: str) -> str:
    path = CHART_DIR / filename
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return str(path)


def plot_monthly_gmv() -> str:
    df = get_monthly_gmv()
    plt.figure(figsize=(12, 6))
    plt.plot(df["month"], df["gmv"], marker="o")
    plt.title("Monthly GMV Trend")
    plt.xlabel("Month")
    plt.ylabel("GMV")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    return _save("monthly_gmv.png")


def plot_top_categories(limit: int = 10) -> str:
    df = get_category_sales_ranking(limit=limit)
    plt.figure(figsize=(12, 6))
    plt.barh(df["product_category_name"], df["gmv"])
    plt.title(f"Top {limit} Categories by GMV")
    plt.xlabel("GMV")
    plt.ylabel("Product Category")
    plt.gca().invert_yaxis()
    return _save("top_categories.png")


def plot_top_states(limit: int = 10) -> str:
    df = get_state_sales_ranking(limit=limit)
    plt.figure(figsize=(10, 6))
    plt.bar(df["customer_state"], df["gmv"])
    plt.title(f"Top {limit} States by GMV")
    plt.xlabel("Customer State")
    plt.ylabel("GMV")
    plt.xticks(rotation=45)
    return _save("top_states.png")


def plot_monthly_orders() -> str:
    df = get_monthly_orders()
    plt.figure(figsize=(12, 6))
    plt.plot(df["month"], df["order_count"], marker="o")
    plt.title("Monthly Order Trend")
    plt.xlabel("Month")
    plt.ylabel("Order Count")
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    return _save("monthly_orders.png")


def plot_payment_type_distribution() -> str:
    df = get_payment_type_distribution()
    plt.figure(figsize=(8, 6))
    plt.bar(df["payment_type"], df["row_count"])
    plt.title("Payment Type Distribution")
    plt.xlabel("Payment Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    return _save("payment_type_distribution.png")


def plot_payment_value_distribution() -> str:
    df = get_payment_type_distribution()
    plt.figure(figsize=(8, 6))
    plt.bar(df["payment_type"], df["total_payment_value"])
    plt.title("Payment Value by Payment Type")
    plt.xlabel("Payment Type")
    plt.ylabel("Total Payment Value")
    plt.xticks(rotation=45)
    return _save("payment_value_distribution.png")


def generate_all_charts() -> dict:
    return {
        "monthly_gmv": plot_monthly_gmv(),
        "top_categories": plot_top_categories(),
        "top_states": plot_top_states(),
        "monthly_orders": plot_monthly_orders(),
        "payment_type_distribution": plot_payment_type_distribution(),
        "payment_value_distribution": plot_payment_value_distribution(),
    }
