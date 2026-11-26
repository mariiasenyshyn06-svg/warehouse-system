from database import db


class DocumentItem(db.Model):
    """Рядок документа: який товар, скільки і за якою ціною."""

    __tablename__ = "document_items"

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    document = db.relationship("Document", back_populates="items")
    product = db.relationship("Product")

    def amount(self):
        """Сума рядка = кількість × ціна."""
        return self.quantity * self.price

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product": self.product.name if self.product else None,
            "sku": self.product.sku if self.product else None,
            "quantity": self.quantity,
            "price": self.price,
            "amount": self.amount(),
        }