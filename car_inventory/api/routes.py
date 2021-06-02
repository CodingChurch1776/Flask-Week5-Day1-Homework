import re
from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import User, Car, car_schema, car_schemas, db

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 73}

#CREATE CAR ENDPOINT
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token): #coming from token_required decorator
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    rear_view_camera = request.json['rear_view_camera']
    miles_per_trip = request.json['miles_per_trip']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_custom = request.json['cost_of_custom']
    make = request.json['make']
    user_token = current_user_token.token

    car = Car(name,description,price,rear_view_camera,miles_per_trip,max_speed,dimensions,weight,cost_of_custom,make,user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Retrieve all cars
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all() 
    response = car_schemas.dump(cars)
    return jsonify(response)

# RETRIEVE ONE CAR ENDPOINT
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

#UPDATE CAR BY ID
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    print(car)
    
    car.name = request.json['name']
    car.description = request.json['description']
    car.price = request.json['price']
    car.rear_view_camera = request.json['rear_view_camera']
    car.miles_per_trip = request.json['miles_per_trip']
    car.max_speed = request.json['max_speed']
    car.dimensions = request.json['dimensions']
    car.weight = request.json['weight']
    car.cost_of_custom = request.json['cost_of_custom']
    car.make = request.json['make']
    car.user_token = current_user_token.token
    print(car.name)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# DELETE CAR BY ID
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = car.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()
        
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error':'This car does not exist'})

