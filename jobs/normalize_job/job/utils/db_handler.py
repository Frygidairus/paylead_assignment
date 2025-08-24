import os

from sqlalchemy import create_engine

# Connection string
DATABASE_URL = os.getenv("DATABASE_URI", "postgresql://admin:adminpass@host.docker.internal:5432/paylead_db")
def get_engine():
    return create_engine(DATABASE_URL)
