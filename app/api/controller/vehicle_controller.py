from flask import request
from flask_restplus import Resource

from ..util.dto import VehicleDto
from ..service.vehicle_service import *

api = VehicleDto.api
_vehicle = VehicleDto.vehicle


@api.route('/')
class VehicleList(Resource):
    @api.doc('list_of_registered_vehicles')
    @api.marshal_list_with(_vehicle, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_vehicles()

    @api.expect(_vehicle, validate=True)
    @api.response(201, 'Vehicle successfully created.')
    @api.doc('create a new Vehicle')
    def post(self):
        """Creates a new Vehicle """
        data = request.json
        return save_new_vehicle(data=data)


@api.route('/<id>')
@api.param('id', 'The Vehicle identifier')
class Vehicle(Resource):
    @api.doc('get a Vehicle')
    @api.marshal_with(_vehicle)
    def get(self, id):
        """get a Vehicle given its identifier"""
        n_id = id if id.isdigit() else 0
        vehicle = get_a_vehicle(n_id)
        if not vehicle:
            return {'success': False, 'message': 'Vehicle not found'}
        else:
            return vehicle


@api.route('/<id>/delete')
@api.param('id', 'The Vehicle identifier')
@api.response(404, 'Vehicle not found.')
class Vehicle(Resource):
    @api.doc('delete a Vehicle')
    def delete(self, id):
        """ Delete Vehicle by id """
        vehicle = get_a_vehicle(int(id))
        if vehicle is not None:
            delete_a_vehicle(vehicle)
            return {'success': True}
        else:
            return {'success': False, 'msg': 'Vehicle does not exist'}
