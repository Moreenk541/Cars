from flask import Blueprint,session,request,jsonify
from models import db
from models.Order import Order
from models.Order_items import OrderItem
from models.Vehicles import Vehicle
from models.Users import User


orders_bp=Blueprint('orders',__name__)

@orders_bp.route('/orders/<int:user_id>',methods=['GET'])
def get_orders(user_id):
    user = User.query.get(user_id)


    if not user:
        return jsonify({'error':'User not found'}),404
    
    orders =Order.query.filter_by(user_id=user.id).all()

    orders_list =[]
    for order in orders:
        items=[]
        for item in order.items:
            items.append({

                "vehicle_id":item.vehicle.id,
                "brand":item.vehicle.brand,
                "model":item.vehicle.model,
                "price_at_purchase":item.price_at_purchase
            })


    orders_list.append({
        "order_id" : order.id,
        "status":order.status,
        "total_price":order.total_price,
        "created_at":order.created_at,
        "items":items


    })


    return jsonify({"orders":orders_list}),200
    

@orders_bp.route('/orders<int:order_id>/status',methods=['PUT']) 
def update_order_status(order_id):
    data =request.json  
    new_status= data.get('status')
    
    valid_statuses =  ['Pending','Paid','Shipped','Delivered','Cancelled']

    if new_status not in valid_statuses:
        return jsonify({'error':'Invalid status'}),400
    
    order =Order.query.get(order_id)

    if not order:
        return jsonify ({'error':'Order not found'})
    
    user_id =session.get(user_id)
    user = User.query.get(user_id)

    if not user or not user.is_admin:
        return jsonify({'error':'Unauthorized'}),403
    

    order.status = new_status
    db.session.commit()

    return jsonify({
        "message":f"Order {order.id}  status updated to {new_status}",
        "order_id":order_id,
        "new_status":new_status
    }),200




