from werkzeug.security import check_password_hash, generate_password_hash

from database import db


class User(db.Model):
    """Користувач системи: комірник, менеджер або адміністратор."""

    __tablename__ = "users"

    ROLES = ("keeper", "manager", "admin")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="keeper")

    def set_password(self, password):
        """Зберігаємо не сам пароль, а його хеш (зашифрований відбиток)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "role": self.role}