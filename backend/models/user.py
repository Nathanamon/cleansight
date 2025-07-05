# backend/models/user.py
from datetime import datetime
from app import db
from models.image import Image
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    agent_code = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    images = db.relationship('Image', backref='user', lazy=True)


    def __repr__(self):
        return (
            f"<User {self.email} | {self.first_name} {self.last_name} | Agent {self.agent_code}>"
        )

    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify the provided password against stored hash.
        """
        return check_password_hash(self.password_hash, password)

    def mark_login(self) -> None:
        """
        Update last_login timestamp to now.
        """
        self.last_login = datetime.utcnow()
        db.session.add(self)
        db.session.commit()