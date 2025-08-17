from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class PointOfSale(db.Model):
    __tablename__ = "point_of_sales"
    id = db.Column(db.Integer, primary_key=True)

    siret = db.Column(db.String(14), index=True, nullable=True)
    store_name = db.Column(db.Text, nullable=False)
    store_name_normalized = db.Column(db.Text, nullable=True)

    street_number = db.Column(db.String(10))
    street = db.Column(db.Text)
    zip_code = db.Column(db.String(6), index=True)
    city = db.Column(db.Text)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)