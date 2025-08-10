from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User:
    _id_counter = 1

    def __init__(self, email, nom, password, role="client"):
        self.id = User._id_counter
        User._id_counter += 1

        self.email = email
        self.nom = nom
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.date_creation = datetime.utcnow()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nom": self.nom,
            "role": self.role,
            "date_creation": self.date_creation.isoformat()
        }
