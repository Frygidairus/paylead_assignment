from flask import Blueprint, request, jsonify
from models import db, PointOfSale


pos = Blueprint('pos', __name__)

@pos.route('/point_of_sales', methods=['POST'])
def create_point_of_sales():

    data = request.json
    pos = PointOfSale(**data)

    db.session.add(pos)
    db.session.commit()

    return jsonify({"id": pos.id, "store_name": pos.store_name}), 201
