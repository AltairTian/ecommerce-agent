from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "database" / "ecommerce.db"

engine = create_engine(f"sqlite:///{DB_PATH}")


TABLES = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_customers_dataset.csv": "customers",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation",
}


def load_csv_to_sqlite():
    for file_name, table_name in TABLES.items():
        file_path = RAW_DATA_DIR / file_name

        if not file_path.exists():
            print(f"跳过：未找到 {file_name}")
            continue

        print(f"正在导入 {file_name} -> {table_name}")

        df = pd.read_csv(file_path)

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )

        print(f"完成：{table_name}, 行数：{len(df)}")

    print(f"数据库已生成：{DB_PATH}")


if __name__ == "__main__":
    load_csv_to_sqlite()