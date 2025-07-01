# backend/utils/tokens.py
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_password_reset_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="password-reset-salt")

def verify_password_reset_token(token: str, expiration: int = 3600) -> str | None:
    """
    Retourne l'email si le token est valide et non expiré (par défaut 1 h), 
    sinon renvoie None.
    """
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt="password-reset-salt",
            max_age=expiration
        )
    except Exception:
        return None
    return email
