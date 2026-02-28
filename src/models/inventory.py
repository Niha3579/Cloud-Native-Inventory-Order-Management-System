from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    stock = Column(Integer, default=0)