from extensions import db

class Medicine(db.Model):
    __tablename__ = 'medicines'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='SET NULL'))
    manufacturer = db.Column(db.String(150))
    batch_number = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    reorder_level = db.Column(db.Integer, nullable=False, default=10)
    expiry_date = db.Column(db.Date)
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "supplier_id": self.supplier_id,
            "manufacturer": self.manufacturer,
            "batch_number": self.batch_number,
            "price": float(self.price) if self.price else 0.0,
            "stock_quantity": self.stock_quantity,
            "reorder_level": self.reorder_level,
            "expiry_date": str(self.expiry_date) if self.expiry_date else None,
            "description": self.description
        }