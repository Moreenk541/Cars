from flask import request,session, jsonify,Blueprint
from models import db
from models.Vehicles import Vehicle
from models.Users import User
from models.Payment import Payment
from models.VehicleImage import VehicleImage
from routes.auth import admin_required
from datetime import datetime


vehicle_bp=Blueprint('Vehicles',__name__)

@vehicle_bp.route('/vehicles',methods=['POST'])
def add_vehicle():
    data = request.json
    user_id= session.get('user_id')


    if not user_id:
        return jsonify({'error':'Login required'}),401
    

    vehicle = Vehicle(
        user_id=user_id,
        type=data['type'],
        brand=data['brand'],
        model=data["model"],
        year=data["year"],
        price=data["price"],
        category=data.get("category"),
        mileage=data.get("mileage"),
        transmission=data["transmission"],
        fuel_type=data["fuel_type"],
        description=data["description"],
        location_city=data.get("location_city"),
        location_region=data.get("location_region"),
        main_image_url=data.get("main_image_url"),
        status='active' if session.get('is_admin') else 'pending'

    )

    db.session.add(vehicle)
    db.session.commit()


    return jsonify({'message':'Vehicle added successfully','id':vehicle.id}),201

#upload images

@vehicle_bp.route('vehicles/int:vehicle_id>/images',methods=['POST'])
def add_images(vehicle_id):
    data= request.json
    images= data.get('images',[])


    for img in images:
        new_image =VehicleImage(vehicle_id=vehicle_id,image_url=img['url'],image_type=img.get('type','other'))
        db.session.add(new_image)

    db.session.commit()
    return jsonify({'message':'Images uploaded successfully'}),201  
        

#admin approval    
@vehicle_bp.route('/vehicles/<int:vehicle_id>/approve',methods=['POST'])
@admin_required    
def approve_vehicle(vehicle_id):
    vehicle=vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({'error':'Vehicle not found'}),404
    
    vehicle.status='approve_waiting_payment'
    vehicle.approval_timestamp = datetime.utcnow()
    db.session.commit()


    return jsonify({'message':'Vehicle approved, waiting for payment'}),200


#Payment
@vehicle_bp.route('/vehicles<int:vehicle_id>/pay',methods=['POST'])
def make_payment(vehicle_id):
    user_id =session.get('user_id')

    if not user_id:
        return jsonify({'error':'Login required'})
    
    vehicle=Vehicle.query.get(vehicle_id)
    if not vehicle or vehicle.status != "approved_awaiting_payment":
        return jsonify({'error':'Vehicle not ready for payment'}),400
    

    data=request.json
    payment=Payment(
        user_id=user_id,
        vehicle_id=vehicle_id,
        amount=data["amount"],
        method=data["method"],
        status="paid",
        transaction_id=data.get("transaction_id")
    )

    vehicle.status = 'active'
    db.session.add(payment)
    db.session.commit()


    return jsonify({'message':'Payment successful, vehicle is now active'})


#view vehicles
@vehicle_bp.route('/vehicles',methods=['GET'])
def view_vehicles():
    query= Vehicle.query.filter_by(status='active')
 
    #Filter
    brand = request.args.get('brand')
    model= request.args.get('model')
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    year = request.args.get("year")

    if brand:
        query = query.filter(Vehicle.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if min_price:
        query = query.filter(Vehicle.price >= float(min_price))
    if max_price:
        query = query.filter(Vehicle.price <= float(max_price))
    if year:
        query = query.filter(Vehicle.year == int(year))

    vehicles = query.all()

    return jsonify([
        {
            "id": v.id,
            "brand": v.brand,
            "model": v.model,
            "year": v.year,
            "price": v.price,
            "main_image": v.main_image_url,
            "location": f"{v.location_city}, {v.location_region}"
        } for v in vehicles
    ])



#vehicle details
@vehicle_bp.route('/vehicles<int:vehicle_id>',methods=['GET'])
def vehicle_details(vehicle_id):
    vehicle =Vehicle.query.get(vehicle_id)

    if not vehicle or vehicle.status != 'active':
        return jsonify({'error':'Vehicle not found'}),404
    

    return jsonify({
        "id": vehicle.id,
        "brand": vehicle.brand,
        "model": vehicle.model,
        "year": vehicle.year,
        "price": vehicle.price,
        "mileage": vehicle.mileage,
        "transmission": vehicle.transmission,
        "fuel_type": vehicle.fuel_type,
        "description": vehicle.description,
        "location": f"{vehicle.location_city}, {vehicle.location_region}",
        "main_image": vehicle.main_image_url,
        "images": [img.image_url for img in vehicle.images]
    })


#soft delete (User)
@vehicle_bp.route("/vehicles/<int:vehicle_id>/deactivate", methods=["PUT"])
def deactivate_vehicle(vehicle_id):
    user_id = session.get("user_id")
    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle or vehicle.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    vehicle.status = "inactive"
    db.session.commit()
    return jsonify({"message": "Vehicle deactivated"})

# --- Hard Delete (Admin) ---
@vehicle_bp.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
@admin_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted"})


    
    
