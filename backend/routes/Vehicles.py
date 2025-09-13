from flask import request,session, jsonify,Blueprint
from models import db
from models.Vehicles import Vehicle
from models.Users import User
from models.Payment import Payment
from models.VehicleImage import VehicleImage
from auth import admin_required


vehicles_bp=Blueprint('Vehicle_bp',__name__)

@vehicles_bp.route('/vehicles',methods=['POST'])
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

@vehicles_bp.route('vehicles/int:vehicle_id>/images',methods=['POST'])
def add_images(vehicle_id):
    data= request.json
    images= data.get('images',[])


    for img in images:
        new_image =VehicleImage(vehicle_id=vehicle_id,image_url=img['url'],image_type=img.get('type','other'))
        db.session.add(new_image)

    db.session.commit()
    return jsonify({'message':'Images uploaded successfully'}),201  
        

#admin approval        