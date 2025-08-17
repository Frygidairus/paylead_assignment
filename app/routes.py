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

@pos.route('/point_of_sales', methods=['GET'])
def list_point_of_sales():

    siret = request.args.get("siret")
    zip_code = request.args.get("zip_code")
    query = PointOfSale.query.filter_by(is_deleted=False)

    if siret:
        query = query.filter_by(siret=siret)

    if zip_code:
        query = query.filter_by(zip_code=zip_code)

    #using list comprehension for better performance
    result = [
        {"id": p.id, "store_name": p.store_name, "siret": p.siret, "zip_code": p.zip_code}
        for p in query.all()
    ]

    return jsonify(result)

@pos.route('/point_of_sales/<int:id>', methods=['GET'])
def get_point_of_sales(id):

    pos = PointOfSale.query.get(id)
    
    if not pos or pos.is_deleted:
        return jsonify({"error": "404 Not found"}), 404
    
    return jsonify({"id": pos.id, "store_name": pos.store_name, "siret": pos.siret})

@pos.route('/point_of_sales/<int:id>', methods=['PUT'])
def update_point_of_sales(id):

    pos = PointOfSale.query.get(id)

    if not pos or pos.is_deleted:
        return jsonify({"error": "Not found"}), 404
    
    data = request.json

    for key, value in data.items():
        setattr(pos, key, value)

    db.session.commit()

    return jsonify({"id": pos.id, "store_name": pos.store_name})