from flask import request,session, jsonify,Blueprint
from models import db
from models.Vehicles import Vehicle
from models.Users import User
from models.Cart import Cart
from models.Cart_items import CartItem


vehicles_bp=Blueprint('Vehicles',__name__)

@vehicles_bp.route("/vehicles",methods=['GET'])
def get_vehicles():
    vehicles =Vehicle.query.all()
    return jsonify([{
        'id': v.id,
        'image': v.image,
        'brand':v.brand,
        'model': v.model,
        'year': v.year,
        'price': v.price,
        'category': v.category,
        'description': v.description

    }for v in vehicles])



@vehicles_bp.route('/search',methods=['GET'])
def search_vehicles():
    query = request.args.get('q','')
    category= request.args.get('category')

    q= Vehicle.query
    if query:
        q=q.filter(Vehicle.model.ilike(f'%{query}%'))
    if category:
        q=q.filter_by(category=category)    

    vehicles=q.all()
    
    return jsonify([{
        'id': v.id, 
        'brand': v.brand,
        'model':v.model,
        "year":v.year,
        'price':v.price
    }for v in vehicles])


