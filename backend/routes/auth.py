# backend/routes/auth.py

import os
from flask import (
    Blueprint, request, jsonify, session,
    url_for, current_app
)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, mail
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ——— Serializer pour les tokens ——————————————————————————————————————————————
def _get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


def generate_password_reset_token(email: str) -> str:
    s = _get_serializer()
    return s.dumps(email, salt="password-reset-salt")


def verify_password_reset_token(token: str, expiration: int = 3600) -> str | None:
    s = _get_serializer()
    try:
        return s.loads(token, salt="password-reset-salt", max_age=expiration)
    except (BadSignature, SignatureExpired):
        return None


# ——— Inscription ——————————————————————————————————————————————————————
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify(error="Email et mot de passe obligatoires"), 400

    if User.query.filter_by(email=email).first():
        return jsonify(error="Cet email est déjà utilisé"), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    # Mail de bienvenue
    try:
        msg = Message(
            subject="🎉 Bienvenue sur CleanSight !",
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email]
        )
        msg.body = (
            f"Bonjour {user.email},\n\n"
            "Merci de vous être inscrit sur CleanSight ! Vous pouvez dès à présent\n"
            "analyser des images et gérer vos poubelles.\n\n"
            "À bientôt,\nL’équipe CleanSight"
        )
        msg.html = (
            f"<p>Bonjour {user.email},</p>"
            "<p>Merci de vous être inscrit sur <strong>CleanSight</strong> ! Vous pouvez dès à présent<br>"
            "analyser des images et gérer vos poubelles.</p>"
            "<p>À bientôt,<br>L’équipe CleanSight</p>"
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.warning(f"Échec envoi mail de bienvenue : {e}")

    return jsonify(
        message="Compte créé avec succès",
        user={"id": user.id, "email": user.email}
    ), 201


# ——— Connexion ——————————————————————————————————————————————————————
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    pwd = data.get("password", "")

    if not email or not pwd:
        return jsonify(error="Email et mot de passe requis"), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, pwd):
        return jsonify(error="Identifiants invalides"), 401

    session.clear()
    session["user_id"] = user.id
    return jsonify(
        message="Connecté",
        user={"id": user.id, "email": user.email}
    ), 200


# ——— Déconnexion / session ——————————————————————————————————————————————————————
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify(message="Déconnecté"), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    uid = session.get("user_id")
    if not uid:
        return jsonify(user=None), 200
    user = User.query.get(uid)
    return jsonify(user={"id": user.id, "email": user.email}), 200


# ——— Mot de passe oublié ——————————————————————————————————————————————————————
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    user = User.query.filter_by(email=email).first()

    # on renvoie toujours 200 pour ne pas exposer l’existence de l’email
    if user:
        token = generate_password_reset_token(user.email)
        reset_url = url_for("auth.reset_password_page", token=token, _external=True)

        msg = Message(
            subject="[CleanSight] Réinitialisation de votre mot de passe",
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email]
        )
        msg.body = (
            f"Bonjour,\n\n"
            f"Pour réinitialiser votre mot de passe, cliquez sur :\n"
            f"{reset_url}\n\n"
            f"Ce lien expirera dans 1 heure.\n"
            f"Si vous n’avez pas demandé cela, ignorez ce message."
        )
        msg.html = (
            "<p>Bonjour,</p>"
            f"<p>Pour réinitialiser votre mot de passe, cliquez <a href='{reset_url}'>ici</a>.</p>"
            "<p>Ce lien expirera dans 1 heure.</p>"
        )
        mail.send(msg)

    return jsonify(
        message="Si cet e-mail existe, vous recevrez un lien sous peu."
    ), 200


# ——— Page de réinitialisation (votre front peut appeler en GET pour vérifier le token) ——
@auth_bp.route("/reset-password/<token>", methods=["GET"])
def reset_password_page(token):
    email = verify_password_reset_token(token)
    if not email:
        return jsonify(error="Lien invalide ou expiré"), 400
    return jsonify(email=email), 200


# ——— Validation du nouveau mot de passe ——————————————————————————————————————————
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    token = data.get("token", "")
    new_pwd = data.get("password", "")

    if not token or not new_pwd:
        return jsonify(error="Token et nouveau mot de passe requis"), 400

    email = verify_password_reset_token(token)
    if not email:
        return jsonify(error="Token invalide ou expiré"), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(error="Utilisateur introuvable"), 404

    user.password_hash = generate_password_hash(new_pwd)
    db.session.commit()
    return jsonify(message="Mot de passe mis à jour."), 200
