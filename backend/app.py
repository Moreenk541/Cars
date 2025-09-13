from  flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import ger_remote_address 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.auth import auth_bp
from routes.Vehicles import vehicles_bp
from models import db





app=Flask(__name__)

limiter = Limiter(
    ger_remote_address,
    app=app,
    default_limits=['200 per day','50 per hour']
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://moreen2:654321@localhost:5432/carsdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)

# Register the auth blueprint
app.register_blueprint(auth_bp,url_prefix="/auth")
app.register_blueprint(vehicles_bp,url_prefix="/vehicles")


with app.app_context():
    db.create_all()

migrate = Migrate(app,db)
@app.route('/')
def message():
    return jsonify({'message': 'Welcome to the home of rides'})

if __name__ =='__main__':
    app.run(debug=True)