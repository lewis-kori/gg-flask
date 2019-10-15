from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    jsonify
)
from flask_login import (
    current_user,
    login_required,

)
from datetime import datetime
from app.models import *
from app.home.forms import *
from app.home.forms import Search, PaymentForm, BookingForm
from sqlalchemy import or_, and_, func

home = Blueprint('home', __name__)


@home.route('/', methods=['post', 'get'])
def index():
    """Admin dashboard page."""
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).limit(8)
    featured_vehicles = Vehicle.query.filter_by(featured=True).limit(4)
    return render_template('home/index.html',
                           all_vehicles=all_vehicles, featured_vehicles=featured_vehicles)


@home.route('/buy_a_car', methods=['post', 'get'])
def inventory():
    """all vehicles."""
    page = request.args.get("page", 1, type=int)
    all_vehicles = (
        Vehicle.query.order_by(Vehicle.createdAt.desc())
        .paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    )
    next_url = (
        url_for("home.inventory", page=all_vehicles.next_num) if all_vehicles.has_next else None
    )
    prev_url = (
        url_for("home.inventory", page=all_vehicles.prev_num) if all_vehicles.has_prev else None
    )
    maxlist = Vehicle.query.order_by(Vehicle.createdAt.desc()).all()
    total_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).all()
    vehicles_count = len(total_vehicles)
    return render_template('home/inventory.html',
                           all_vehicles=all_vehicles.items, vehicles_count=vehicles_count, next_url=next_url,
                           prev_url=prev_url, maxlist=maxlist)


@home.route('/view_car/<id>', methods=['post', 'get'])
def view_car(id):
    """Admin dashboard page."""
    more_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).limit(3)
    vehicle = Vehicle.query.get_or_404(id)
    fuel_id = vehicle.fuel_type_id
    car_fuel_type = Fuel.query.filter_by(id=fuel_id).first_or_404()
    return render_template('home/single_car_view.html',
                           more_vehicles=more_vehicles, vehicle=vehicle, car_fuel_type=car_fuel_type)


@home.route('/contact_us')
def contact():
    return render_template('home/contact_us.html')


@home.route('/blog')
def blog():
    return render_template('home/blog.html')


@home.route('/single_post')
def single_post():
    return render_template('home/single_post.html')


@home.route('/privacy_policy')
def privacy():
    return render_template('home/privacy_policy.html')


@home.route('/terms-of-use')
def terms_of_use():
    return render_template('home/terms_of_use.html')


@home.route('/terms-and-conditions')
def tour_operators_terms():
    return render_template('home/tour_operators_terms.html')


@home.route("/sell_your_car", methods=["GET", "POST"])
def sell_vehicle():
    all_vehicles = Vehicle.query.all()
    """sell a vehicle."""
    form = SellVehicleForm()
    form.make.choices = [(row.id, row.name) for row in Make.query.all()]
    form.model.choices = [(row.id, row.name) for row in Model.query.all()]
    form.transmission.choices = [(row.id, row.type) for row in Transmission.query.all()]
    form.fuel_type.choices = [(row.id, row.type) for row in Fuel.query.all()]
    if form.validate_on_submit():
        make = Make.query.filter_by(id=form.make.data).first_or_404()
        model = Model.query.filter_by(id=form.model.data).first_or_404()
        transmission = Transmission.query.filter_by(
            id=form.transmission.data
        ).first_or_404()
        fuel = Fuel.query.filter_by(id=form.fuel_type.data).first_or_404()
        new_vehicle = SellersVehicle(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            plate=form.plate.data,
            year=form.year.data,
            mileage=form.mileage.data,
            color=form.color.data,
            condition=form.condition.data,
            seller_name=form.seller_name.data,
            seller_email=form.seller_email.data,
            phone_number=form.phone_number.data,
            area=form.area.data,
            model_id=model.id,
            make_id=make.id,
            transmission_id=transmission.id,
            fuel_type_id=fuel.id,
            interior=form.interior.data,
            engine_size=form.engine_size.data,
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for("home.index"))
    return render_template("home/sell_vehicle.html", form=form)


@home.route("/imports", methods=["GET", "POST"])
def import_vehicle():
    all_vehicles = Vehicle.query.all()
    """import a vehicle."""
    form = ImportVehicleForm()
    form.make.choices = [(row.id, row.name) for row in Make.query.all()]
    form.model.choices = [(row.id, row.name) for row in Model.query.all()]
    form.transmission.choices = [(row.id, row.type) for row in Transmission.query.all()]
    form.fuel_type.choices = [(row.id, row.type) for row in Fuel.query.all()]
    if form.validate_on_submit():
        make = Make.query.filter_by(id=form.make.data).first_or_404()
        model = Model.query.filter_by(id=form.model.data).first_or_404()
        transmission = Transmission.query.filter_by(
            id=form.transmission.data
        ).first_or_404()
        fuel = Fuel.query.filter_by(id=form.fuel_type.data).first_or_404()
        new_vehicle = SellersVehicle(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            plate=form.plate.data,
            year=form.year.data,
            mileage=form.mileage.data,
            color=form.color.data,
            condition=form.condition.data,
            seller_name=form.seller_name.data,
            seller_email=form.seller_email.data,
            phone_number=form.phone_number.data,
            area=form.area.data,
            model_id=model.id,
            make_id=make.id,
            transmission_id=transmission.id,
            fuel_type_id=fuel.id,
            interior=form.interior.data,
            engine_size=form.engine_size.data,
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for("home.index"))
    return render_template("home/import.html", form=form)



@home.route("/_get_model")
def _get_model():
    make_id = request.args.get("make_id", 0, type=int)
    models = [
        (row.id, row.name) for row in Model.query.filter_by(make_id=make_id).all()
    ]
    return jsonify(models)
