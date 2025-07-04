from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from sqlalchemy import func, case
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


@dashboard_bp.route("/daily", methods=["GET"])
def daily_stats():
    """Return counts of full and empty bins per day."""
    days = int(request.args.get("days", 7))
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)

    results = (
        db.session.query(
            func.date(Image.date_upload).label("date"),
            func.sum(case((Image.annotation == "pleine", 1), else_=0)).label("full"),
            func.sum(case((Image.annotation == "vide", 1), else_=0)).label("empty"),
        )
        .filter(Image.date_upload >= start_date)
        .group_by(func.date(Image.date_upload))
        .order_by(func.date(Image.date_upload))
        .all()
    )

    data_map = {}
    for row in results:
        data_map[row.date] = {"full": row.full, "empty": row.empty}

    labels = []
    full = []
    empty = []
    current = start_date
    while current <= end_date:
        labels.append(current.isoformat())
        stats = data_map.get(current, {"full": 0, "empty": 0})
        full.append(stats["full"])
        empty.append(stats["empty"])
        current += timedelta(days=1)

    return jsonify({"labels": labels, "full": full, "empty": empty}), 200


@dashboard_bp.route("/accuracy", methods=["GET"])
def classification_accuracy():
    """Return daily classification accuracy stats."""
    days = int(request.args.get("days", 5))
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)

    results = (
        db.session.query(
            func.date(Image.date_upload).label("date"),
            func.sum(case((Image.annotation == Image.annotation_auto, 1), else_=0)).label(
                "correct"
            ),
            func.sum(case((Image.annotation != Image.annotation_auto, 1), else_=0)).label(
                "incorrect"
            ),
        )
        .filter(Image.date_upload >= start_date)
        .group_by(func.date(Image.date_upload))
        .order_by(func.date(Image.date_upload))
        .all()
    )

    data_map = {}
    for row in results:
        data_map[row.date] = {"correct": row.correct, "incorrect": row.incorrect}

    labels = []
    correct = []
    incorrect = []
    current = start_date
    while current <= end_date:
        labels.append(current.isoformat())
        stats = data_map.get(current, {"correct": 0, "incorrect": 0})
        correct.append(stats["correct"])
        incorrect.append(stats["incorrect"])
        current += timedelta(days=1)

    return jsonify({"labels": labels, "correct": correct, "incorrect": incorrect}), 200
