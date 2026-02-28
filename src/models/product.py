from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from src.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)