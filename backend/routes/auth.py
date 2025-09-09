from flask import Blueprint, request, jsonify, session
from models import db
from models.Users import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signUp',methods=['POST'])
def signUp():
    
    data =request.json
    if not data.get('username')  or not data.get ('email') or not data.get('password'):
        return jsonify({'error':'Missing fields'}),400
    
    if User.query.filter((User.username == data['username']) | (User.email ==data['email'])).first():
        return jsonify({'error':'User already exists'}),400
    
    user =User(username=data['username'], email =data['email'])
    user.password=data['password']

    db.session.add(user)
    db.session.commit()

    return jsonify({'message':'User registered successfully'}),201


@auth_bp.route('/login',methods=['POST','GET'])
def login():

    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()


    if user and user.check_password(data.get('password')):
        session['user_id']=user.id
        return jsonify({'message':'Login successful', 'user':user.username}),200
    
    return jsonify({'error':'Invalid email or password'}),401

@auth_bp.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id',None)
    return jsonify({'message':"Logged out"}),200








