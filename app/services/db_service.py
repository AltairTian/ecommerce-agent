from pathlib import Path
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "database" / "ecommerce.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

# from app.services.db_service import engine