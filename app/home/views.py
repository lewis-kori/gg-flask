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
    form = Search()
    """Admin dashboard page."""
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).limit(5)
    return render_template('home/index.html', form=form,
                           all_vehicles=all_vehicles)


@home.route('/privacy_policy')
def privacy():
    return render_template('home/privacy_policy.html')


@home.route('/terms-of-use')
def terms_of_use():
    return render_template('home/terms_of_use.html')


@home.route('/tour-operators/terms-and-conditions')
def tour_operators_terms():
    return render_template('home/tour_operators_terms.html')
