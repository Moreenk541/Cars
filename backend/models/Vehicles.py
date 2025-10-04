from . import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Enum('car', 'bike', name='vehicle_type'), nullable=False)
    brand = db.Column(db.String(400), nullable=False)
    model = db.Column(db.String(400), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.String(500), nullable=False)
    mileage = db.Column(db.Integer, nullable=True)
    transmission = db.Column(db.Enum("automatic", "manual", name="transmission_type"), nullable=False)
    fuel_type = db.Column(db.Enum("petrol", "diesel", "electric", "hybrid", name="fuel_type"), nullable=False)
    location_city = db.Column(db.String(100))
    location_region = db.Column(db.String(100))
    main_image_url = db.Column(db.String(255), nullable=True)
    status = db.Column(
        db.Enum("pending", "approved_awaiting_payment", "active", "inactive", "rejected", name="vehicle_status"),
        default="pending",
        nullable=False
    )

    approval_timestamp = db.Column(db.DateTime, nullable=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="vehicles")
    cart_items = db.relationship("CartItem", back_populates="vehicle", cascade="all, delete-orphan")
    order_items = db.relationship("OrderItem", back_populates="vehicle", cascade="all, delete-orphan")
    images = db.relationship("VehicleImage", back_populates="vehicle", cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="vehicle")
