from extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    status = db.Column(db.Enum('pending', 'confirmed', 'dispatched', 'delivered', 'cancelled', 'completed'), nullable=False, default='pending')
    delivery_address = db.Column(db.Text)
    order_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "total_amount": float(self.total_amount),
            "status": self.status,
            "delivery_address": self.delivery_address,
            "order_date": str(self.order_date)
        }