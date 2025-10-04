from . import db

class CartItem(db.Model):
    __tablename__ ='cart_items'

    id = db.Column(db.Integer,primary_key=True)
    cart_id=db.Column(db.Integer,db.ForeignKey('cart.id'),nullable=False)
    vehicle_id=db.Column(db.Integer,db.ForeignKey('vehicles.id'),nullable=False)
    quantity=db.Column(db.Integer,default=1,nullable=False)

    #relationships
    cart = db.relationship('Cart', back_populates='items')
    vehicle = db.relationship('Vehicle', back_populates='cart_items')

    