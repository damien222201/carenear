"""Shared helpers: email validation, rate limiting, place rollups."""
import re
from datetime import datetime, timedelta
from models import db, PlaceReport

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

RATE_LIMIT_WINDOW_MINUTES = 60
RATE_LIMIT_MAX_REPORTS = 5

# "Open now" status is very time-sensitive — shorter staleness window than
# the outage tracker (LightWatch uses 12h; this uses 6h).
STATUS_STALE_HOURS = 6


def is_valid_email(email):
    return bool(email) and bool(EMAIL_RE.match(email.strip()))


def is_rate_limited(email, ip_address):
    window_start = datetime.utcnow() - timedelta(minutes=RATE_LIMIT_WINDOW_MINUTES)
    count = PlaceReport.query.filter(
        PlaceReport.created_at >= window_start,
        db.or_(PlaceReport.email == email, PlaceReport.ip_address == ip_address),
    ).count()
    return count >= RATE_LIMIT_MAX_REPORTS


def places_for_state(state, place_type=None):
    """All places reported in a state, grouped by name with latest status, best (open, freshest) first."""
    query = PlaceReport.query.filter_by(state=state)
    if place_type:
        query = query.filter_by(place_type=place_type)
    reports = query.order_by(PlaceReport.created_at.desc()).all()

    grouped = {}
    for r in reports:
        key = r.place_name.strip().lower()
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(r)

    stale_cutoff = datetime.utcnow() - timedelta(hours=STATUS_STALE_HOURS)
    results = []
    for key, items in grouped.items():
        latest = items[0]  # already sorted newest-first
        is_stale = latest.created_at < stale_cutoff
        results.append({
            "place_name": latest.place_name,
            "place_type": latest.place_type,
            "area": latest.area,
            "latest_status": latest.status,
            "is_24hr": latest.is_24hr,
            "is_stale": is_stale,
            "last_report_at": latest.created_at,
            "note": latest.note,
            "lat": latest.lat,
            "lon": latest.lon,
            "report_count": len(items),
        })

    # Sort: fresh-and-open first, then fresh-and-closed, then stale/unknown last
    def sort_key(item):
        if item["is_stale"]:
            return 2
        return 0 if item["latest_status"] == "open" else 1
    results.sort(key=sort_key)
    return results
