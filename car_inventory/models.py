from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid #stands for unique user id - WILL use for Primary Keys

#Adding Flask Security for password protection - 
from werkzeug.security import generate_password_hash, check_password_hash

#import secrets module (provided by)
import secrets


from flask_login import UserMixin, LoginManager

#Install Our Marshaller
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User: {self.email} has been created and added to the database!"


class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision = 10, scale = 2))
    rear_view_camera = db.Column(db.String(120), nullable = True)
    miles_per_trip = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_custom = db.Column(db.Numeric(precision = 10, scale = 2))
    make = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, rear_view_camera, miles_per_trip, max_speed, dimensions, weight, cost_of_custom, make, user_token, id = ''):
            self.id = self.set_id()
            self.name = name
            self.description = description
            self.price = price
            self.rear_view_camera = rear_view_camera
            self.miles_per_trip = miles_per_trip
            self.max_speed = max_speed
            self.dimensions = dimensions
            self.weight = weight
            self.cost_of_custom = cost_of_custom
            self.make = make
            self.user_token = user_token

    def __repr__(self):
        return f'The following car has been created: {self.name}'
    
    def set_id(self):
        return str(uuid.uuid4())

# API Schema via Marshmallow
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'rear_view_camera', 'miles_per_trip', 'max_speed', 'dimensions', 'weight', 'cost_of_custom', 'make']

# Singular data point return
car_schema = CarSchema()

# List of multiple onjects returned
car_schemas = CarSchema(many = True)