from flask_restplus import Api
from flask import Blueprint

import os

from .controller.vehicle_controller import api as vehicle_ns

basedir = os.path.abspath(os.path.dirname(__file__))


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='API',
          version='1.0',
          description='GIGI API VERSION ONE'
          )

api.add_namespace(vehicle_ns, path='/api/v1/vehicle')
