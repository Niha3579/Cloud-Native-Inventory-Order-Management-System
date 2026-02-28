from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.user import User
from src.models.order import Order

router = APIRouter()

@router.post("/orders")
def create_order(user_id: int, db: Session = Depends(get_db)):

    new_order = Order(user_id=user_id)

    db.add(new_order)
    db.commit()

    return {"message": "Order created"}


@router.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):

    result = db.query(Order).join(User).filter(Order.id == order_id).first()

    return result