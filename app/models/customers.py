import uuid
from pydantic import BaseModel
from sqlalchemy import Column, String
from app.db.db import Base


class Customer(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class CustomerInfo(Customer):
    id: str


class CustomerDB(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=lambda: uuid.uuid4().hex, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
