from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,

)
from flask_login import (
    current_user,
    login_required,

)
from datetime import datetime
from app.models import *
from app.home.forms import Search, PaymentForm, BookingForm
from sqlalchemy import or_, and_, func

home = Blueprint('home', __name__)


@home.route('/', methods=['post', 'get'])
def index():
    """Admin dashboard page."""
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).limit(5)
    return render_template('home/index.html',
                           all_vehicles=all_vehicles)


@home.route('/view_car/<id>', methods=['post', 'get'])
def view_car(id):
    """Admin dashboard page."""
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).limit(5)
    vehicle = Vehicle.query.get_or_404(id)
    fuel_id = vehicle.fuel_type_id
    car_fuel_type = Fuel.query.filter_by(id=fuel_id).first_or_404()
    return render_template('home/single_car_view.html',
                           all_vehicles=all_vehicles, vehicle=vehicle, car_fuel_type=car_fuel_type)


@home.route('/contact_us')
def contact():
    return render_template('home/contact_us.html')


@home.route('/privacy_policy')
def privacy():
    return render_template('home/privacy_policy.html')


@home.route('/terms-of-use')
def terms_of_use():
    return render_template('home/terms_of_use.html')


@home.route('/terms-and-conditions')
def tour_operators_terms():
    return render_template('home/tour_operators_terms.html')
