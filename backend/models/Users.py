from models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"


    id =db.Column(db.Integer,primary_key=True) 
    username = db.Column(db.String(100),unique =True, nullable=False)
    email=db.Column(db.String(155),unique=True, nullable=False)
    _password_hash = db.Column('password',db.String(255),unique=True,nullable= False)
    is_admin =db.Column(db.Boolean,default=False,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)

    #relationships
    cart =db.relationship('Cart',back_populates='user',uselist=False)
    orders = db.relationship('Order', back_populates='user')


    @property
    def password(self):
        raise AttributeError ('Password is write-only.')
    
    @password.setter
    def password(self,plain_password):
        self._password_hash=generate_password_hash(plain_password)

    #password verification
    def check_password(self,password)    :
        return check_password_hash(self._password_hash,password)