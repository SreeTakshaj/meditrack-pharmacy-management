from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.medicine import Medicine
from utils.auth_helper import role_required

medicine_bp = Blueprint('medicines', __name__)

# ---------------------------------------------------------
# Route: Get all medicines (Anyone can view)
# GET /api/medicines
# ---------------------------------------------------------
@medicine_bp.route('/', methods=['GET'])
def get_all_medicines():
    medicines = Medicine.query.all()
    return jsonify([med.to_dict() for med in medicines]), 200

# ---------------------------------------------------------
# Route: Add a new medicine (Admin/Pharmacist only)
# POST /api/medicines
# ---------------------------------------------------------
@medicine_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['admin', 'pharmacist'])
def add_medicine():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({"error": "Missing required fields (name, price)"}), 400

    new_med = Medicine(
        name=data['name'],
        price=data['price'],
        category_id=data.get('category_id'),
        supplier_id=data.get('supplier_id'),
        manufacturer=data.get('manufacturer'),
        batch_number=data.get('batch_number'),
        stock_quantity=data.get('stock_quantity', 0),
        reorder_level=data.get('reorder_level', 10),
        expiry_date=data.get('expiry_date'),
        description=data.get('description')
    )

    try:
        db.session.add(new_med)
        db.session.commit()
        return jsonify({"message": "Medicine added successfully", "medicine": new_med.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------
# Route: Update a medicine (Admin/Pharmacist only)
# PUT /api/medicines/<id>
# ---------------------------------------------------------
@medicine_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'pharmacist'])
def update_medicine(id):
    med = Medicine.query.get(id)
    if not med:
        return jsonify({"error": "Medicine not found"}), 404

    data = request.get_json()
    
    # Update fields if they are provided
    med.name = data.get('name', med.name)
    med.price = data.get('price', med.price)
    med.stock_quantity = data.get('stock_quantity', med.stock_quantity)
    med.reorder_level = data.get('reorder_level', med.reorder_level)
    
    db.session.commit()
    return jsonify({"message": "Medicine updated", "medicine": med.to_dict()}), 200

# ---------------------------------------------------------
# Route: Delete a medicine (Admin only)
# DELETE /api/medicines/<id>
# ---------------------------------------------------------
@medicine_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_medicine(id):
    med = Medicine.query.get(id)
    if not med:
        return jsonify({"error": "Medicine not found"}), 404

    db.session.delete(med)
    db.session.commit()
    return jsonify({"message": "Medicine deleted successfully"}), 200