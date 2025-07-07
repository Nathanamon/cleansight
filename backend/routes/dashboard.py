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
    emptied_bins = Image.query.filter_by(annotation="vidée").count()
    return jsonify({
        "total_images": total_images,
        "empty_bins": empty_bins,
        "full_bins": full_bins,
        "emptied_bins": emptied_bins,
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
        location = None
        if img.metadata_json:
            loc = img.metadata_json.get("location", {})
            location = loc.get("address")

        data.append({
            "id": img.id,
            "filename": img.filename,
            "annotation": img.annotation,
            "date_upload": img.date_upload.isoformat(),
            "location": location,
        })
    return jsonify(data), 200


@dashboard_bp.route("/weather_trash", methods=["GET"])
def weather_trash():
    """Return daily counts of full bins and average humidity."""
    days = int(request.args.get("days", 5))
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)

    images = Image.query.filter(Image.date_upload >= start_date).all()

    data_map = {}
    for img in images:
        day = img.date_upload.date()
        entry = data_map.setdefault(day, {"full": 0, "humidity_sum": 0, "cnt": 0})
        if img.annotation == "pleine":
            entry["full"] += 1
        try:
            humidity = img.metadata_json.get("weather", {}).get("humidity")
        except AttributeError:
            humidity = None
        if humidity is not None:
            entry["humidity_sum"] += float(humidity)
            entry["cnt"] += 1

    labels = []
    full = []
    humidity = []
    current = start_date
    while current <= end_date:
        stats = data_map.get(current, {})
        labels.append(current.isoformat())
        full.append(stats.get("full", 0))
        if stats.get("cnt"):
            humidity.append(round(stats["humidity_sum"] / stats["cnt"], 2))
        else:
            humidity.append(0)
        current += timedelta(days=1)

    return jsonify({"labels": labels, "full": full, "humidity": humidity}), 200


@dashboard_bp.route("/fill_rate", methods=["GET"])
def fill_rate():
    """Return average fill rate by city."""
    images = Image.query.filter(Image.metadata_json.isnot(None)).all()
    stats = {}
    for img in images:
        try:
            addr = img.metadata_json.get("location", {}).get("address", "")
            city = addr.split(",")[1].strip() if "," in addr else "?"
        except Exception:
            city = "?"
        entry = stats.setdefault(city, {"total": 0, "full": 0})
        entry["total"] += 1
        if img.annotation == "pleine":
            entry["full"] += 1

    labels = []
    rate = []
    for city, val in stats.items():
        labels.append(city)
        r = round((val["full"] / val["total"] * 100), 2) if val["total"] else 0
        rate.append(r)

    return jsonify({"labels": labels, "rate": rate}), 200


@dashboard_bp.route("/peak_hours", methods=["GET"])
def peak_hours():
    """Return fill rate per time slot."""
    slots = [(0, 6), (6, 9), (9, 12), (12, 15), (15, 18), (18, 21), (21, 24)]
    labels = []
    rates = []
    for start, end in slots:
        total = (
            db.session.query(func.count(Image.id))
            .filter(func.extract("hour", Image.date_upload) >= start)
            .filter(func.extract("hour", Image.date_upload) < end)
            .scalar()
        )
        full = (
            db.session.query(func.count(Image.id))
            .filter(func.extract("hour", Image.date_upload) >= start)
            .filter(func.extract("hour", Image.date_upload) < end)
            .filter(Image.annotation == "pleine")
            .scalar()
        )
        rate = round((full / total * 100), 2) if total else 0
        labels.append(f"{start:02d}h-{end % 24:02d}h")
        rates.append(rate)

    return jsonify({"labels": labels, "rate": rates}), 200


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


@dashboard_bp.route("/map", methods=["GET"])
def map_data():
    """Return list of trash bins with coordinates."""
    images = (
        Image.query
        .filter(Image.metadata_json.isnot(None))
        .filter(Image.annotation != "vide")
        .order_by(Image.date_upload.desc())
        .all()
    )
    data = []
    for img in images:
        try:
            location = img.metadata_json.get("location", {})
            lat = location.get("lat")
            lon = location.get("lon")
            address = location.get("address")
            if lat is not None:
                lat = float(lat)
            if lon is not None:
                lon = float(lon)
        except (AttributeError, ValueError, TypeError):
            lat = lon = address = None

        if lat is not None and lon is not None:
            data.append({
                "id": img.id,
                "latitude": lat,
                "longitude": lon,
                "address": address,
                "etat": img.annotation,
                "timestamp": img.date_upload.isoformat(),
            })
    return jsonify(data), 200