from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from .base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")