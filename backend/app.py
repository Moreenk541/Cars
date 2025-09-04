from  flask import Flask, jsonify
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://moreen2:654321@localhost:5432/carsdb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app,db)
@app.route('/')
def message():
    return jsonify({'message': 'Welcome to the home of rides'})

if __name__ =='__main__':
    app.run(debug=True)