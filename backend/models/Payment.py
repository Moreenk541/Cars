from . import db
from datetime import datetime



class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.Enum("mpesa", "paypal", "card", name="payment_method"), nullable=False)
    status = db.Column(db.Enum("pending", "paid", "failed", name="payment_status"), default="pending", nullable=False)
    transaction_id = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    vehicle = db.relationship("Vehicle", back_populates="payments")
    user = db.relationship("User", back_populates="payments")