from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.product import Product
from src.schemas.product_schema import ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.put("/{product_id}")
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)
    return {"message": "Updated"}


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}