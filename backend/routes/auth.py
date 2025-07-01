# backend/routes/auth.py
from flask import Blueprint, request, jsonify, session
from app import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email et mot de passe obligatoires"}), 400

    # Vérifie qu'on n'a pas déjà cet email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Cet email est déjà utilisé"}), 409

    # Crée l'utilisateur
    hashed = generate_password_hash(password)
    user = User(email=email, password_hash=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Compte créé avec succès", "user": {"id": user.id, "email": user.email}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    pwd   = data.get("password", "")

    if not email or not pwd:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(pwd):
        return jsonify({"error": "Identifiants invalides"}), 401

    session.clear()
    session["user_id"] = user.id
    return jsonify({"message": "Connecté", "user": {"id": user.id, "email": user.email}}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Déconnecté"}), 200

@auth_bp.route("/me", methods=["GET"])
def me():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"user": None}), 200
    u = User.query.get(uid)
    return jsonify({"user": {"id": u.id, "email": u.email}}), 200
