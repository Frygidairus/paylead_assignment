import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://admin:adminpass@localhost:5432/paylead_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False