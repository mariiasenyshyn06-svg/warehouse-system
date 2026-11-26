from datetime import datetime

from database import db


class Document(db.Model):
    """Документ складу: прибуткова накладна, видаткова накладна або акт списання."""

    __tablename__ = "documents"

    TYPES = {
        "incoming": "Прибуткова накладна",
        "outgoing": "Видаткова накладна",
        "write_off": "Акт списання",
    }

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(30), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)
    counterparty_id = db.Column(db.Integer, db.ForeignKey("counterparties.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)

    supplier = db.relationship("Supplier")
    counterparty = db.relationship("Counterparty")
    user = db.relationship("User")
    # Композиція: рядки документа не існують без самого документа
    items = db.relationship("DocumentItem", back_populates="document",
                            cascade="all, delete-orphan")
    movements = db.relationship("StockMovement", back_populates="document")

    def title(self):
        """Назва документа українською."""
        return self.TYPES.get(self.type, self.type)

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "type": self.type,
            "title": self.title(),
            "date": self.date.strftime("%d.%m.%Y %H:%M"),
            "supplier": self.supplier.name if self.supplier else None,
            "counterparty": self.counterparty.name if self.counterparty else None,
            "user": self.user.username if self.user else None,
            "total": self.total,
            "items": [item.to_dict() for item in self.items],
        }