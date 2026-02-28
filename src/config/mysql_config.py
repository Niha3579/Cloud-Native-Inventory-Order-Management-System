import os
from sqlalchemy import create_engine
from src.config.settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE

# 1. Check if an environment variable override exists (used for CI testing)
# If os.getenv("MYSQL_URL") is empty, it falls back to your settings.py variables
DATABASE_URL = os.getenv(
    "MYSQL_URL", 
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# 2. SQLite needs a specific connect_arg to work with FastAPI during testing
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# 3. Create the engine, passing the connect_args
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)