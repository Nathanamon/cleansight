import os
import json
from flask import Blueprint, current_app, request, jsonify
from utils.rules import load_rules_from_json

rules_bp = Blueprint("rules", __name__)


@rules_bp.route("/rules", methods=["GET"])
def get_rules():
    rules_path = os.path.join(current_app.root_path, "utils", "rules.json")
    with open(rules_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@rules_bp.route("/rules", methods=["PUT"])
def update_rules():
    rules_path = os.path.join(current_app.root_path, "utils", "rules.json")
    rules = request.get_json()
    if not isinstance(rules, list):
        return jsonify({"error": "Invalid rules format"}), 400
    with open(rules_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)
    load_rules_from_json(rules_path)
    return jsonify({"status": "ok"})