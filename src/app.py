from fastapi import FastAPI
from src.config.mysql_config import engine
from sqlalchemy import text
from src.models.base import Base
from src.models import product
from src.routes.user_routes import router as user_router
from src.routes.product_routes import router as product_router
from src.routes.order_routes import router as order_router
from fastapi.staticfiles import StaticFiles
from src.routes.auth_routes import router as auth_router



import src.models.user
import src.models.product
import src.models.order
import src.models.order_item
import src.models.inventory

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(auth_router)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/mysql-test")
def mysql_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
    return {"mysql_connection": "success"}


from src.config.mongo_config import mongo_db

@app.get("/mongo-test")
def mongo_test():
    mongo_db.test_collection.insert_one({"message":"mongo connected"})
    return {"mongodb":"connected"}


@app.get("/")
def home():
    return {"message": "Inventory System Running"}