from datetime import datetime

from database import db


class Notification(db.Model):
    """Сповіщення для менеджера, наприклад про мінімальний запас товару."""

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_read = db.Column(db.Boolean, nullable=False, default=False)

    product = db.relationship("Product")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product": self.product.name if self.product else None,
            "message": self.message,
            "created_at": self.created_at.strftime("%d.%m.%Y %H:%M"),
            "is_read": self.is_read,
        }