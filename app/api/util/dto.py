from flask_restplus import Namespace, fields
from app.models import *


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'id': fields.Integer,
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class VehicleDto:
    api = Namespace('vehicle', description='vehicle related operations')
    vehicle = api.model('vehicle', {
        'id': fields.Integer,
        'name': fields.String(required=True, description='The vehicle name '),
        'price': fields.String(description='The vehicle password '),
        'description': fields.String(required=True, description='The vehicle description '),
        'plate': fields.String(description='The vehicle plate '),
        'year': fields.String(required=True, description='The vehicle year'),
        'image_url': fields.String(required=True, description='The vehicle image '),
        'back_image_url': fields.String(description='The vehicle back image '),
        'dash_image_url': fields.String(description='The vehicle dash image '),
        'front_image_url': fields.String(description='The vehicle front image '),
        'interior_image_url': fields.String(description='The vehicle interior image '),
        'left_image_url': fields.String(description='The vehicle left image '),
        'right_image_url': fields.String(description='The vehicle right image '),
        'mileage': fields.String(description='The vehicle mileage'),
        'color': fields.String(description='The vehicle color '),
        'condition': fields.String(description='The vehicle condition'),
        'seller_name': fields.String(description='The vehicle seller name '),
        'seller_email': fields.String(description='The vehicle seller image '),
        'phone_number': fields.String(description='The vehicle phone number'),
        'area': fields.String(description='The vehicle area'),
        'model_id': fields.String(description='The vehicle model'),
        'make_id': fields.String(description='The vehicle make'),
        'transmission_id': fields.String(description='The vehicle transmission'),
        'fuel_type_id': fields.String(description='The vehicle fuel type'),
        'interior': fields.String(description='The vehicle interior'),
        'engine_size': fields.String(description='The vehicle engine')
    })
