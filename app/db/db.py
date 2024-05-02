from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DatabaseConfig

SQLALCHEMY_DATABASE_URL = f"postgresql://{DatabaseConfig.DB_USERNAME}:{DatabaseConfig.DB_PASSWORD}@{DatabaseConfig.DB_HOST}:{DatabaseConfig.DB_PORT}/{DatabaseConfig.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
