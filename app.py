"""
CareNear
--------
Crowdsourced open/closed status for pharmacies, hospitals, and clinics in
Nigeria. No live API exists that reliably tells you whether a specific
pharmacy is open right now — opening-hours data, where it exists at all,
goes stale fast. CareNear is self-reported by design, same pattern as the
rest of this project series, with a free Leaflet/OpenStreetMap view and
browser-geolocation-based "nearest" sorting on top.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from models import db, PlaceReport
from reference_data import STATES, PLACE_TYPES, STATE_CENTERS
from utils import is_valid_email, is_rate_limited, places_for_state


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    database_url = os.environ.get("DATABASE_URL", "sqlite:///carenear_dev.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        total_reports = PlaceReport.query.count()
        return render_template(
            "index.html", states=STATES, place_types=PLACE_TYPES, total_reports=total_reports,
        )

    @app.route("/report", methods=["POST"])
    def report():
        email = request.form.get("email", "").strip()
        state = request.form.get("state", "").strip()
        area = request.form.get("area", "").strip()
        place_name = request.form.get("place_name", "").strip()
        place_type = request.form.get("place_type", "").strip()
        status = request.form.get("status", "").strip()
        is_24hr = request.form.get("is_24hr") == "yes"
        lat_raw = request.form.get("lat", "").strip()
        lon_raw = request.form.get("lon", "").strip()
        note = request.form.get("note", "").strip() or None
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("index"))
        if state not in STATES:
            flash("Please select a valid state.", "error")
            return redirect(url_for("index"))
        if not area or len(area) > 200:
            flash("Please enter the area.", "error")
            return redirect(url_for("index"))
        if not place_name or len(place_name) > 200:
            flash("Please enter the pharmacy/hospital/clinic name.", "error")
            return redirect(url_for("index"))
        if place_type not in PLACE_TYPES:
            flash("Please select a valid place type.", "error")
            return redirect(url_for("index"))
        if status not in ("open", "closed"):
            flash("Please select the current status.", "error")
            return redirect(url_for("index"))
        if is_rate_limited(email, ip_address):
            flash("You've submitted a few reports recently — please wait a bit before reporting again.", "error")
            return redirect(url_for("index"))

        lat = lon = None
        try:
            if lat_raw and lon_raw:
                lat, lon = float(lat_raw), float(lon_raw)
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    lat = lon = None
        except ValueError:
            lat = lon = None

        new_report = PlaceReport(
            email=email, state=state, area=area, place_name=place_name,
            place_type=place_type, status=status, is_24hr=is_24hr,
            lat=lat, lon=lon, note=note, ip_address=ip_address,
        )
        db.session.add(new_report)
        db.session.commit()

        flash("Thanks — your report has been added.", "success")
        return redirect(url_for("index"))

    @app.route("/browse")
    def browse():
        state = request.args.get("state", "").strip()
        place_type = request.args.get("place_type", "").strip()
        if place_type and place_type not in PLACE_TYPES:
            place_type = ""

        results = places_for_state(state, place_type or None) if state in STATES else []
        center = STATE_CENTERS.get(state, STATE_CENTERS["Lagos"])

        return render_template(
            "browse.html", states=STATES, place_types=PLACE_TYPES,
            state=state, place_type=place_type, results=results, center=center,
        )

    @app.route("/api/places")
    def api_places():
        state = request.args.get("state", "").strip()
        query = PlaceReport.query
        if state in STATES:
            query = query.filter_by(state=state)
        reports = query.order_by(PlaceReport.created_at.desc()).limit(300).all()
        return jsonify([r.to_dict() for r in reports])

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
