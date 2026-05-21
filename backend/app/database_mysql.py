import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    tidb_host = os.getenv("TIDB_HOST")
    tidb_port = os.getenv("TIDB_PORT", "4000")
    tidb_user = os.getenv("TIDB_USER")
    tidb_password = os.getenv("TIDB_PASSWORD")
    tidb_database = os.getenv("TIDB_DATABASE", "test")

    if tidb_host and tidb_user and tidb_password:
        DATABASE_URL = (
            f"mysql+pymysql://{tidb_user}:{tidb_password}"
            f"@{tidb_host}:{tidb_port}/{tidb_database}?charset=utf8mb4&ssl=true"
        )
    else:
        DATABASE_URL = "sqlite:///./local_demo.db"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {"ssl": {"ssl": True}}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            print(f"Database connection OK: {DATABASE_URL.split('@')[-1]}")
            return True
    except Exception as exc:
        print(f"Database connection failed: {exc}")
        return False


def create_tables():
    Base.metadata.create_all(bind=engine)
