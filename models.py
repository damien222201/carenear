"""Database model for CareNear."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PlaceReport(db.Model):
    __tablename__ = "place_reports"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    state = db.Column(db.String(50), nullable=False, index=True)
    area = db.Column(db.String(200), nullable=False)
    place_name = db.Column(db.String(200), nullable=False, index=True)
    place_type = db.Column(db.String(10), nullable=False, index=True)  # "pharmacy" | "hospital" | "clinic"
    status = db.Column(db.String(10), nullable=False)  # "open" | "closed"
    is_24hr = db.Column(db.Boolean, nullable=False, default=False)
    lat = db.Column(db.Float, nullable=True)
    lon = db.Column(db.Float, nullable=True)
    note = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    @property
    def place_key(self):
        return f"{self.state}|{self.place_name.strip().lower()}"

    def to_dict(self):
        return {
            "id": self.id,
            "state": self.state,
            "area": self.area,
            "place_name": self.place_name,
            "place_type": self.place_type,
            "status": self.status,
            "is_24hr": self.is_24hr,
            "lat": self.lat,
            "lon": self.lon,
            "note": self.note,
            "created_at": self.created_at.isoformat() + "Z",
        }
