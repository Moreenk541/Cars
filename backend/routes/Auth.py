from flask import Blueprint, request, jsonfiy, session
from app import db
from models.Users import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signUp',methods=['POST'])
def signUp():
    
    data =request.json
    if not data.get('username')  or not data.get ('email') or not data.get('password'):
        return jsonfiy({'error':'Missing fields'}),400
    
    if User.query.filter((User.username == data['username']) | (User.email ==data['email'])).first():
        return jsonfiy({'error':'User already exists'}),400
    
    user =User(username=data['username'], email =data['email'])
    user.password=data['password']

    db.session.add(user)
    db.session.commit()

    return jsonfiy({'message':'User registered successfully'}),200


@auth_bp.route('/login',methods='[POST]')
def login():
    







