from app import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key =True)
    type=db.Column(db.Enum('Vehicle','bike', name='Vehicle_type'),nullable=False)
    brand=db.Column(db.String(400),nullable=False)
    model =db.Column(db.String(400),nullable=False)
    year=db.Column(db.Integer, nullable= False)
    Price= db.Column(db.Integer,nullable= False)
    category = db.Column(db.String(50)) 
    description = db.Column(db.String(500),nullable=False)
    image_url=db.Column(db.String(255),nullable=False)
    created_at=db.Column(db.datetime,default=datetime.utcnow, nullable=False)

    #relationships 
    cart_items= db.relationship('CartItem',back_populates='vehicle')
    order_items=db.relationship('OrderItem',back_populates='vehicle')
                                


    