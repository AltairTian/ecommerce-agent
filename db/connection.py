"""数据库连接管理 —— 所有 SQL 查询通过这里获取连接。"""

import sqlite3
import pandas as pd
from config.settings import DB_PATH


def get_connection() -> sqlite3.Connection:
    """返回 SQLite 连接。调用方负责关闭。"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def query_db(sql: str) -> pd.DataFrame:
    """执行 SQL 查询并返回 DataFrame。"""
    conn = get_connection()
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()
