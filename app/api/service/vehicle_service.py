import uuid
import datetime
from app import db
from app.models.vehicle import Vehicle


def save_new_vehicle(data):
    vehicle = Vehicle.query.filter_by(name=data['name']).first()
    if not vehicle:
        new_vehicle = Vehicle(
            name=data['name'],
            price=data['price'],
            description=data['description'],
            plate=data['plate'],
            year=data['year'],
            image_url=data['front_image'],
            back_image_url=data['back_image'],
            dash_image_url=data['dash_image'],
            front_image_url=data['front_image'],
            interior_image_url=data['interior_image'],
            left_image_url=data['left_image'],
            right_image_url=data['right_image'],
            mileage=data['mileage'],
            color=data['color'],
            condition=data['condition'],
            seller_name=data['seller_name'],
            seller_email=data['seller_email'],
            phone_number=data['phone_number'],
            area=data['area'],
            model_id=data['model_id'],
            make_id=data['make_id'],
            transmission_id=data['transmission_id'],
            fuel_type_id=data['fuel_id'],
            interior=data['interior'],
            engine_size=data['engine_size'],
        )
        save_changes(new_vehicle)
        return generate_vehicle(new_vehicle)

    else:
        response_object = {
            'status': 'fail',
            'message': 'Vehicle already exists.'
        }
        return response_object, 409


def get_all_vehicles():
    return Vehicle.query.all()


def get_a_vehicle(id):
    return Vehicle.query.get_or_404(id)


def generate_vehicle(vehicle):
    try:
        response_object = {
            'status': 'success',
            'message': 'Vehicle Successfully registered.',
            'data': {
                'name': vehicle.name,
                'price': vehicle.price,
                'description': vehicle.description,
                'plate': vehicle.plate,
                'year': vehicle.year,
                'image_url': vehicle.front_image_url,
                'back_image_url': vehicle.back_image_url,
                'dash_image_url': vehicle.dash_image_url,
                'front_image_url': vehicle.front_image_url,
                'interior_image_url': vehicle.interior_image_url,
                'left_image_url': vehicle.left_image_url,
                'right_image_url': vehicle.right_image_url,
                'mileage': vehicle.mileage,
                'color': vehicle.color,
                'condition': vehicle.condition,
                'seller_name': vehicle.seller_name,
                'seller_email': vehicle.seller_email,
                'phone_number': vehicle.phone_number,
                'area': vehicle.area,
                'model_id': vehicle.model_id,
                'make_id': vehicle.make_id,
                'transmission_id': vehicle.transmission_id,
                'fuel_type_id': vehicle.fuel_type_id,
                'interior': vehicle.interior_image_url,
                'engine_size': vehicle.engine_size
            }
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def delete_a_vehicle(id):
    vehicle = get_a_vehicle(id)
    db.session.delete(vehicle)
    db.session.commit()
    try:
        response_object = {
            'status': 'success',
            'message': 'Vehicle Successfully deleted.'
        }
        return response_object, 204
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()


