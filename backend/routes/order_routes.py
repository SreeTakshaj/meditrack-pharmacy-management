from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.order import Order
from models.order_item import OrderItem
from models.medicine import Medicine
from models.user import User
from utils.auth_helper import role_required
from datetime import datetime

order_bp = Blueprint('orders', __name__)

# GET recent orders (For Dashboard)
@order_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin', 'pharmacist'])
def get_recent_orders():
    # Get the 5 most recent orders
    orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    result = []
    for order in orders:
        customer = User.query.get(order.customer_id)
        result.append({
            "id": order.id,
            "customer_name": customer.name if customer else "Unknown",
            "total_amount": float(order.total_amount),
            "status": order.status,
            "date": order.order_date.strftime("%Y-%m-%d %H:%M")
        })
    return jsonify(result), 200

# POST create a new order (Deducts stock)
@order_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['admin', 'pharmacist', 'customer'])
def create_order():
    data = request.get_json()
    current_user_id = int(get_jwt_identity())

    if not data or not data.get('items'):
        return jsonify({"error": "No items in order"}), 400

    try:
        total_amount = 0
        order_items = []

        # 1. Check stock and calculate total
        for item in data['items']:
            med = Medicine.query.get(item['medicine_id'])
            if not med:
                return jsonify({"error": f"Medicine ID {item['medicine_id']} not found"}), 404
            
            if med.stock_quantity < item['quantity']:
                return jsonify({"error": f"Insufficient stock for {med.name}"}), 400

            total_amount += (med.price * item['quantity'])
            
            # Deduct stock
            med.stock_quantity -= item['quantity']
            
            order_items.append({
                "medicine_id": med.id,
                "quantity": item['quantity'],
                "unit_price": med.price
            })

        # 2. Create Order
        new_order = Order(
            customer_id=current_user_id,
            total_amount=total_amount,
            status='delivered'  # Auto-complete for demo purposes
        )
        db.session.add(new_order)
        db.session.flush() # Get the order ID before committing

        # 3. Create Order Items
        for oi in order_items:
            new_item = OrderItem(
                order_id=new_order.id,
                medicine_id=oi['medicine_id'],
                quantity=oi['quantity'],
                unit_price=oi['unit_price']
            )
            db.session.add(new_item)

        db.session.commit()
        return jsonify({"message": "Order placed successfully", "order_id": new_order.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500