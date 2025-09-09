from app import db
from datetime import datetime


class OrderItem(db.Model):
    __tablename__='order_items'

    id =db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'),nullable=False)
    vehicle_id=db.Column(db.Integer,db.ForeignKey('vehicle.id'),nullable=False)
    price_at_purchase=db.Column(db.Integer,nullable=False)

    #relationships
    order = db.relationship('Order', back_populates='items')
    vehicle = db.relationship('Vehicle', back_populates='order_items')

    