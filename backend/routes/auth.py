# backend/routes/auth.py
import re
from datetime import timedelta
from flask import Blueprint, request, jsonify, url_for, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, unset_jwt_cookies,
    set_access_cookies, set_refresh_cookies, get_csrf_token
)
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from main import db, mail
from models.user import User
from config import Config

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ——— Serializer pour les tokens —————————————————————————————————————————————
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

# ——— Inscription —————————————————————————————————————————————————————
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password", "")
    agent_code = (data.get("agent_code") or "").strip().upper()
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()

    # Champs requis
    if not email or not password or not agent_code or not first_name or not last_name:
        return jsonify(error="Email, mot de passe, nom et code agent obligatoires"), 400

    # Validation email
    if not re.fullmatch(r"[a-z0-9._-]+@paris\.fr", email):
        return jsonify(error="Email non autorisé, doit finir par @paris.fr"), 403

    # Validation agent code
    if not re.fullmatch(Config.AGENT_CODE_PATTERN, agent_code):
        return jsonify(error="Code agent invalide, format AGP-xxxx"), 403

    # Duplicate email
    if User.query.filter_by(email=email).first():
        return jsonify(error="Cet email est déjà utilisé"), 409

    # Création utilisateur
    user = User(
        email=email,
        agent_code=agent_code,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Envoi mail de bienvenue
    try:
        msg = Message(
            subject="🎉 Bienvenue sur CleanSight !",
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email]
        )
        msg.body = (
            f"Bonjour {user.email},\n\n"
            "Merci de vous être inscrit sur CleanSight ! Vous pouvez dès à présent analyser vos images.\n\n"
            "À bientôt,\nL’équipe CleanSight"
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.warning(f"Échec envoi mail de bienvenue : {e}")

    return jsonify(message="Compte créé avec succès"), 201

# ——— Connexion —————————————————————————————————————————————————————
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)  # force = parse même si content-type est absent ou mauvais
    except Exception as e:
        current_app.logger.error(f"[LOGIN] Erreur parsing JSON: {e}")
        return jsonify(error="Requête invalide (format JSON)"), 422

    email = (data.get("email") or "").strip().lower()
    password = data.get("password", "")
    agent_code = (data.get("agent_code") or "").strip().upper()
    remember_me = data.get("remember_me", False)

    # Champs requis
    if not email or not password or not agent_code:
        return jsonify(error="Email, mot de passe et code agent requis"), 400

    # Validation email et code
    if not re.fullmatch(r"[a-z0-9._-]+@paris\.fr", email):
        return jsonify(error="Email non autorisé"), 403
    if not re.fullmatch(Config.AGENT_CODE_PATTERN, agent_code):
        return jsonify(error="Code agent invalide"), 403

    user = User.query.filter_by(email=email, agent_code=agent_code).first()
    if not user:
        return jsonify(error="Compte inexistant"), 404
    if not user.check_password(password):
        return jsonify(error="Mot de passe incorrect"), 401

    # ——— DUREE SELON "remember_me" ———
    if remember_me:
        expires = timedelta(days=14)       # 2 semaines si souvenir
    else:
        expires = timedelta(hours=2)       # 2h sinon

    # Créer tokens
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    refresh_token = create_refresh_token(identity=str(user.id), expires_delta=expires)


    resp = jsonify(
        message="Connecté",
        user={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        csrf_token=get_csrf_token(access_token)
    )
    # On ajoute les tokens dans la réponse
    
    # Utilise les helpers JWT pour définir aussi le cookie CSRF
    set_access_cookies(resp, access_token, max_age=int(expires.total_seconds()))
    set_refresh_cookies(resp, refresh_token, max_age=int(expires.total_seconds()))
    return resp, 200


# ——— Refresh token ———————————————————————————————————————————————————
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_token = create_access_token(identity=identity, expires_delta=timedelta(hours=2))
    resp = jsonify(
        message="Token rafraîchi",
        csrf_token=get_csrf_token(new_token)
    )
    set_access_cookies(resp, new_token, max_age=2 * 3600)
    return resp, 200

# ——— Déconnexion ——————————————————————————————————————————————————————
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    resp = jsonify(message="Déconnecté")
    unset_jwt_cookies(resp)
    return resp, 200

# ——— Profil utilisateur —————————————————————————————————————————————————
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(user=None), 404
    return jsonify(
        user={
            "id": user.id,
            "email": user.email,
            "agent_code": user.agent_code,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    ), 200

# ——— Mot de passe oublié ——————————————————————————————————————————————————————
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    user = User.query.filter_by(email=email).first()
    # On renvoie toujours 200 pour protéger l'existence
    if user:
        token = generate_password_reset_token(user.email)
        reset_url = url_for("auth.reset_password_page", token=token, _external=True)
        msg = Message(
            subject="[CleanSight] Réinitialisation de votre mot de passe",
            sender=current_app.config["MAIL_DEFAULT_SENDER"],
            recipients=[user.email]
        )
        msg.body = (
            f"Bonjour,\n\nVeuillez réinitialiser votre mot de passe via : {reset_url}\n"
            "Ce lien expire en 1 heure."
        )
        mail.send(msg)
    return jsonify(message="Si cet email existe, vous recevrez un lien sous peu."), 200

# ——— Vérification du token —————————————————————————————————————————————————
@auth_bp.route("/reset-password/<token>", methods=["GET"])
def reset_password_page(token):
    email = verify_password_reset_token(token)
    if not email:
        return jsonify(error="Lien invalide ou expiré"), 400
    return jsonify(email=email), 200

# ——— Réinitialisation du mot de passe —————————————————————————————————————————————
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    token = data.get("token", "")
    new_pwd = data.get("password", "")
    if not token or not new_pwd:
        return jsonify(error="Token et mot de passe requis"), 400
    email = verify_password_reset_token(token)
    if not email:
        return jsonify(error="Token invalide ou expiré"), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(error="Utilisateur introuvable"), 404
    user.set_password(new_pwd)
    db.session.commit()
    return jsonify(message="Mot de passe mis à jour."), 200