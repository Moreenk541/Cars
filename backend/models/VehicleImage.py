from app import db
from datetime import datetime

class VehicleImage(db.Model):
    __tablename__ = "vehicle_images"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    image_type = db.Column(db.Enum("main", "rear", "interior", "side", "other", name="image_type"), default="other")

    vehicle = db.relationship("Vehicle", back_populates="images")
