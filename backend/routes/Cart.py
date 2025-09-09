from flask import request, jsonify, Blueprint
from models import db
from models.Users import User
from models.Vehicles import Vehicle
from models.Cart import Cart
from models.Cart_items import CartItem
from models.Order import Order
from models.Order_items import OrderItem

cart_bp = Blueprint("cart", __name__)

@cart_bp.route('/<int:vehicle_id>/add-to-cart', methods=['POST'])
def add_to_cart(vehicle_id):
    user_id = request.json.get('user_id')
    quantity = request.json.get('quantity', 1)  # default to 1

    user = User.query.get(user_id)
    vehicle = Vehicle.query.get(vehicle_id)

    if not user or not vehicle:
        return jsonify({"error": "User or vehicle not found"}), 404

    
    if not user.cart:
        user.cart = Cart(user=user)
        db.session.add(user.cart)
        db.session.commit()

    # Check if this vehicle is already in the cart
    cart_item = CartItem.query.filter_by(cart_id=user.cart.id, vehicle_id=vehicle.id).first()

    if cart_item:
        cart_item.quantity += quantity  # increase quantity
    else:
        cart_item = CartItem(cart=user.cart, vehicle=vehicle, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        "message": f"{vehicle.brand} added to {user.username}'s cart",
        "vehicle": vehicle.brand,
        "quantity": cart_item.quantity
    }), 200



@cart_bp.route('/<int:vehicle_id>/remove-from-cart',methods=['POST'])
def remove_from_cart(vehicle_id):
    user_id=request.json.get('user_id')
    quantity= request.json.get('quantity',1)

    user = User.query.get(user_id)

    if not user or not user.cart:
        return jsonify({'error':'User or cart not found'}),404
    

    cart_item =CartItem.query.filter_by(cart_id =user.cart.id, vehicle_id=vehicle_id).first()
    if not cart_item:
        return jsonify({'error':'Item not in the cart'}),404
    

    if cart_item.quantity > quantity:
        cart_item.quantity -= quantity

    else:
        db.session.delete(cart_item)    


    db.session.commit()
    return jsonify({"message":"Item removed from the cart"}),200



@cart_bp.route('/<int:user_id>/cart', methods=['GET'])
def view_cart(user_id):
    user=User.query.get(user_id)

    if not user or not user.cart:
        return jsonify({"error":'User or Cart not found'}),404
    
    cart_items = CartItem.query.filter_by(cart_id=user.cart.id).all()
    cart_data =[]
    total_price = 0

    for item in cart_items:
        vehicle = Vehicle.query.get(item.vehicle_id)
        item_total = vehicle. price *item.quantity
        total_price += item_total

        cart_data.append({
            "vehicle_id":vehicle.id,
            "brand":vehicle.brand,
            "model":vehicle.model,
            "price":vehicle.price,
            "quantity":item.quantity,
            "item_total":item_total
        })

    return jsonify({
        "user":user.username,
        "items":cart_data,
        "total_price": total_price
    }) ,200      


@cart_bp.route('/<int:vehcle_id>/update-cart',methods=['POST'])
def update_cart(vehicle_id):
    user_id =request.json.get('user_id')
    new_quantity = request.json.get('quantity')

    if new_quantity is None or new_quantity < 1:
        return jsonify({"error":"Quantity must be >= 1"}),400
    
    user =User.query.get(user_id)
    if not user or not user.cart:
        return jsonify({'error':'User or Cart not found'}),404
    
    cart_item =  CartItem.query.filter_by(cart_id=user.cart.id)

    if not cart_item:
        return  jsonify({"error": "Item not in cart"}),404
    
    cart_item.quantity = new_quantity
    db.session.commit()


    return jsonify({"message":f"Quantity updated {new_quantity}"}),200




@cart_bp.route('/checkout',methods=['POST'])
def checkout():
    user_id = request.json.get('user_id')
    user =User.query.get(user_id)


    if not user:
        return jsonify({"error": "user not found"}),404
    
    if not user.cart or not user.cart.items:

        return jsonify({"error":"cart not found"}),404
    

    #create order
    order =Order(user_id=user.id, total_price=0,status="Pending")

    db.session.add(order)

    total_price =0

    for item in user.cart.items:
        order_item = OrderItem(
            order=order,
            vehicle=item.vehicle,
            price_at_purchase=item.vehicle.price
        )

        db.session.add(order_item)

        total_price += item.vehicle.price * item.quantity


    order.total_price = total_price


    user.cart.items.clear()

    db.session.commit()


    return jsonify({
        'message':'Checkout successful',
        'order_id':order.id,
        'total_price':total_price
    }),201
    





