from flask import Blueprint, jsonify, request
from app import db
from models.image import Image

# Blueprint for dashboard related endpoints
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/summary", methods=["GET"])
def summary():
    """Return aggregate counts for the dashboard."""
    total_images = Image.query.count()
    empty_bins = Image.query.filter_by(annotation="vide").count()
    full_bins = Image.query.filter_by(annotation="pleine").count()
    return jsonify({
        "total_images": total_images,
        "empty_bins": empty_bins,
        "full_bins": full_bins,
    }), 200

@dashboard_bp.route("/recent", methods=["GET"])
def recent():
    """Return most recently uploaded images."""
    limit = int(request.args.get("limit", 5))
    images = (
        Image.query.order_by(Image.date_upload.desc())
        .limit(limit)
        .all()
    )
    data = []
    for img in images:
        data.append({
            "id": img.id,
            "filename": img.filename,
            "annotation": img.annotation,
            "date_upload": img.date_upload.isoformat(),
        })
    return jsonify(data), 200
