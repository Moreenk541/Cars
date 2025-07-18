from app import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ ='cart'

    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    created_at=db.Column(db.datetime,default=datetime.utcnow,nullable=False)

    #relationships

    user = db.relationship('User',back_populates='cart')
    items=db.relationship('CartItem',back_populates='cart',cascade='all,delete-orphan')