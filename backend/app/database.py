import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # For assignment review, set DATABASE_URL to PostgreSQL/MySQL in .env.
    # Local fallback keeps the app runnable for quick demos.
    "sqlite:///./hcp_crm.db",
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
