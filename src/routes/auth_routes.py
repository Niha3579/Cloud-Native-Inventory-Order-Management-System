from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.user import User
from src.schemas.user_schema import UserRegister, UserLogin
from src.mongo_db import logs_collection

router = APIRouter(prefix="/users", tags=["Authentication"])


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    # store login log in MongoDB
    logs_collection.insert_one({
        "user_id": db_user.id,
        "email": db_user.email,
        "action": "login"
    })

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "name": db_user.name
    }