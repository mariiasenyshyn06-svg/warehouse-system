from database import db


class Counterparty(db.Model):
    """Контрагент: клієнт або партнер, якому відвантажують товар."""

    __tablename__ = "counterparties"

    KINDS = ("client", "partner")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    kind = db.Column(db.String(30), default="client")
    phone = db.Column(db.String(30))
    email = db.Column(db.String(120))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "phone": self.phone,
            "email": self.email,
        }