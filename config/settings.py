"""
统一配置模块 —— 所有配置从 .env 读取，提供默认值。
项目中所有其他模块从这里获取配置，杜绝硬编码。
"""

import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

# Ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0"))

# 数据库
DB_PATH = PROJECT_ROOT / "db" / "ecommerce.db"

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"

# LangSmith
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")


def print_config() -> None:
    """调试用：打印当前配置。"""
    print("OLLAMA_MODEL:", OLLAMA_MODEL)
    print("OLLAMA_BASE_URL:", OLLAMA_BASE_URL)
    print("DB_PATH:", DB_PATH)
    print("CHART_DIR:", CHART_DIR)
    print("LANGSMITH_TRACING:", LANGSMITH_TRACING)
    print("LANGSMITH_PROJECT:", LANGSMITH_PROJECT)
