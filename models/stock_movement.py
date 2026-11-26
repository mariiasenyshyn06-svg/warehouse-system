from datetime import datetime

from database import db


class StockMovement(db.Model):
    """Запис про рух товару: надходження, відвантаження або списання."""

    __tablename__ = "stock_movements"

    TYPES = ("incoming", "outgoing", "write_off")

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    product = db.relationship("Product")
    document = db.relationship("Document", back_populates="movements")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product": self.product.name if self.product else None,
            "document_id": self.document_id,
            "document_number": self.document.number if self.document else None,
            "type": self.type,
            "quantity": self.quantity,
            "date": self.date.strftime("%d.%m.%Y %H:%M"),
        }