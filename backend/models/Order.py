from . import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    total_price = db.Column(db.Integer, nullable=False)
    status=db.Column(db.Enum('Pending','Paid','Shipped','Delivered','Cancelled',default='Pending', name='order_status'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)



    #relationships
    user = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")