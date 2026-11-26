from database import db


class Product(db.Model):
    """Товар на складі."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)  # артикул
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    min_quantity = db.Column(db.Integer, nullable=False, default=5)

    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    supplier = db.relationship("Supplier", back_populates="products")

    def is_low_stock(self):
        """GRASP Information Expert: товар сам знає, чи мало його залишилось."""
        return self.quantity <= self.min_quantity

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "quantity": self.quantity,
            "price": self.price,
            "min_quantity": self.min_quantity,
            "supplier_id": self.supplier_id,
            "supplier": self.supplier.name if self.supplier else None,
            "low_stock": self.is_low_stock(),
        }