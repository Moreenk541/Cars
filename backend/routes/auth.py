from flask import session, request,jsonify,Blueprint
from models import db
from models.Users import User
from app import limiter
from functools import wraps

auth_bp=Blueprint('auth',__name__)

#ADMIN DECORATOR

def admin_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        user_id =session.get('user_id')
        is_admin= session.get('is_admin')

        if not user_id or not is_admin:
            return jsonify({'error':'Admin access required'}),403
        
        return f(*args,**kwargs)
    
    return decorated_function


#Sign up

@auth_bp.route('/signUp',methods=['POST'])
@limiter.limit("5 per 30 mimunites")
def signUp():
    data = request.json

    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error':'Missing fields'}),400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first() :
        return jsonify({'error':'User already exists'})
    
    user = User(
        username =data['username'],
        email=data['email']
    )
    user.password =data['password']

    if data['email'].endswith('.admin.com'):
        user.is_admin= True

    db.session.add(user) 
    db.session.commit()   

    return jsonify({'message':'User registered successfully'}),200



#Login
@auth_bp.route('/login',methods=['POST'])
@limiter.limit(' 5 per minute')
def login():
    data = request.json
    user = User.query.filter_by(email=data.get(['email'])).first()

    if user and user.check_password(data.get('password')):
        session['user_id'] = user.id
        session['is_admin'] =user.is_admin
        return jsonify({'message':'Login successful','user':user.username,'is_admin':user.is_admin}),200
    
    return jsonify ({'error':'Invalid email or password'}),400

#Logout
@auth_bp.route('/logout',methods=['POST'])    
def logout():
    session.pop('user_id',None)
    session.pop('is_admin',None)
    return jsonify({'message':'Logged out'}),200

#change password
@auth_bp.router('/change-password',methods=['POST'])
@limiter.limit('3 per hour')
def change_password():
    data = request.json
    user_id =session.get('user_id')

    if not user_id:
        return jsonify({'error':'Not logged in'}),401
    
    user = User.query.get('user_id')
    if not user:
        return jsonify({'error':'User not found'}),404
    
    old_password =data.get('old-password')
    new_password =data.get('new_password')

    if not user.check_password(old_password):
        return jsonify({'error':'Old password is incorrect'}),400
    
    user.password =new_password
    db.session.commit()


    return jsonify({'message':'Password changed successfully'}),201


@auth_bp.route('/forgot-password',methods=['POST'])
@limiter.limit('3 per hour')
def forgot_password():
    data = request.json
    email = data.get['email']
    new_password =data.get['new_password']


    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error':'User not found'})
    
    user.passord =new_password
    db.session.commit()


    return jsonify({'message':'Password reset successful'})




    

