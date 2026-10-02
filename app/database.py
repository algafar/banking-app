from sqlalchemy.orm import sessionmaker,DeclarativeBase
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from app.config import setting

safe_password = quote_plus(setting.DB_PASSWORD)

DATABASE_URL = (
    f"mysql+pymysql://{setting.DB_USER}:"
    f"{safe_password}@"
    f"{setting.DB_HOST}:"
    f"{setting.DB_PORT}/"
    f"{setting.DB_NAME}"
)

engine = create_engine(DATABASE_URL,pool_pre_ping=True,pool_recycle=3600)

SessionLocal = sessionmaker(bind=engine,autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()