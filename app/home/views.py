from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required
from datetime import datetime, date
from app.models import *
from app.home.forms import *
from sqlalchemy import or_, and_, func

home = Blueprint("home", __name__)


@home.route("/", methods=["post", "get"])
def index():
    """Admin dashboard page."""
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).limit(8)
    featured_vehicles = Vehicle.query.filter_by(featured=True).limit(8)
    form = SearchForm()
    make = [(row.id, row.name) for row in Make.query.all()]
    model = [(row.id, row.name) for row in Model.query.all()]
    transmission = [(row.id, row.type) for row in Transmission.query.all()]
    fuel = [(row.id, row.type) for row in Fuel.query.all()]
    year_to = [(i, i) for i in list(reversed(range(2000, date.today().year)))]
    year_from = [(i, i) for i in list(reversed(range(2000, date.today().year)))]
    make.insert(0, (0, "--All Makes--"))
    year_from.insert(0, (0, "Year from"))
    year_to.insert(0, (0, "Year to"))
    model.insert(0, (0, "Model"))
    transmission.insert(0, (0, "Transmission"))
    fuel.insert(0, (0, "Fuel Type"))
    form.year_from.choices = year_from
    form.year_to.choices = year_to
    form.make.choices = make
    form.model.choices = model
    form.transmission.choices = transmission
    form.fuel.choices = fuel
    return render_template(
        "home/index.html",
        all_vehicles=all_vehicles,
        featured_vehicles=featured_vehicles,
        form=form,
        car_makes=Make.query.all(),
    )


@home.route("/buy_a_car", methods=["post", "get"])
def inventory():
    """all vehicles."""
    page = request.args.get("page", 1, type=int)
    year_from = request.args.get("year_from", 0, type=int)
    year_to = request.args.get("year_to", 0, type=int)
    make = request.args.get("make", 0, type=int)
    model = request.args.get("model", 0, type=int)
    fuel = request.args.get("fuel", 0, type=int)
    transmission = request.args.get("transmission", 0, type=int)

    makes = [(row.id, row.name) for row in Make.query.all()]
    transmissions = [(row.id, row.type) for row in Transmission.query.all()]
    fuel_types = [(row.id, row.type) for row in Fuel.query.all()]
    years = list(reversed(range(2005, date.today().year)))

    all_vehicles = (
        Vehicle.query.filter(
            Vehicle.year >= year_from if year_from else Vehicle.id.isnot(None)
        )
        .filter(Vehicle.year <= year_to if year_to else Vehicle.id.isnot(None))
        .filter(Vehicle.make_id == make if make else Vehicle.id.isnot(None))
        .filter(Vehicle.model_id == model if model else Vehicle.id.isnot(None))
        .filter(
            Vehicle.transmission_id == transmission
            if transmission
            else Vehicle.id.isnot(None)
        )
        .filter(Vehicle.fuel_type_id == fuel if fuel else Vehicle.id.isnot(None))
        .order_by(Vehicle.createdAt.desc())
        .paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    )
    next_url = (
        url_for("home.inventory", page=all_vehicles.next_num)
        if all_vehicles.has_next
        else None
    )
    prev_url = (
        url_for("home.inventory", page=all_vehicles.prev_num)
        if all_vehicles.has_prev
        else None
    )
    total_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).all()
    vehicles_count = len(all_vehicles.items)
    max_price = int(max(node.price for node in total_vehicles)) if total_vehicles else 0
    min_price = int(min(node.price for node in total_vehicles)) if total_vehicles else 0
    return render_template(
        "home/inventory.html",
        all_vehicles=all_vehicles.items,
        vehicles_count=vehicles_count,
        next_url=next_url,
        prev_url=prev_url,
        max_price=max_price,
        min_price=min_price,
        makes=makes,
        transmissions=transmissions,
        years=years,
        fuel_types=fuel_types,
    )


@home.route("/_get_cars/", methods=["POST"])
def _get_cars():
    page = request.args.get("page", 1, type=int)
    data = request.get_json() or {}
    if (
        "years" not in data
        or "makes" not in data
        or "models" not in data
        or "transmissions" not in data
        or "min_price" not in data
        or "max_price" not in data
    ):
        return "", 404
    all_vehicles = (
        Vehicle.query.filter(
            Vehicle.year.in_(data["years"])
            if len(data["years"])
            else Vehicle.id.isnot(None)
        )
        .filter(
            Vehicle.make_id.in_(data["makes"])
            if len(data["makes"])
            else Vehicle.id.isnot(None)
        )
        .filter(
            Vehicle.model_id.in_(data["models"])
            if len(data["models"])
            else Vehicle.id.isnot(None)
        )
        .filter(
            Vehicle.transmission_id.in_(data["transmissions"])
            if len(data["transmissions"])
            else Vehicle.id.isnot(None)
        )
        .filter(
            Vehicle.price >= data["min_price"]
            if data["min_price"]
            else Vehicle.id.isnot(None)
        )
        .filter(
            Vehicle.price <= data["max_price"]
            if data["max_price"]
            else Vehicle.id.isnot(None)
        )
        .order_by(Vehicle.createdAt.desc())
        .paginate(page, current_app.config["POSTS_PER_PAGE"], False)
    )
    next_url = (
        url_for("home.inventory", page=all_vehicles.next_num)
        if all_vehicles.has_next
        else None
    )
    prev_url = (
        url_for("home.inventory", page=all_vehicles.prev_num)
        if all_vehicles.has_prev
        else None
    )
    return render_template(
        "home/_inventory.html",
        all_vehicles=all_vehicles.items,
        vehicles_count=len(all_vehicles.items),
        next_url=next_url,
        prev_url=prev_url,
    )


@home.route("/view_car/<id>", methods=["post", "get"])
def view_car(id):
    """Admin dashboard page."""

    vehicle = Vehicle.query.get_or_404(id)
    fuel_id = vehicle.fuel_type_id
    more_vehicles = (
        Vehicle.query.filter_by(make_id=vehicle.make_id)
        .order_by(Vehicle.createdAt.desc())
        .limit(3)
    )
    car_fuel_type = Fuel.query.filter_by(id=fuel_id).first_or_404()
    return render_template(
        "home/single_car_view.html",
        more_vehicles=more_vehicles,
        vehicle=vehicle,
        car_fuel_type=car_fuel_type,
    )


@home.route("/contact_us")
def contact():
    return render_template("home/contact_us.html")


@home.route("/blog")
def blog():
    return render_template("home/blog.html")


@home.route("/single_post")
def single_post():
    return render_template("home/single_post.html")


@home.route("/privacy_policy")
def privacy():
    return render_template("home/privacy_policy.html")


@home.route("/terms-of-use")
def terms_of_use():
    return render_template("home/terms_of_use.html")


@home.route("/terms-and-conditions")
def tour_operators_terms():
    return render_template("home/tour_operators_terms.html")


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


@home.route("/_get_models", methods=["POST"])
def _get_models():
    makes = request.get_json()["makes"]
    models = [
        (row.id, row.name) for row in Model.query.filter(Model.make_id.in_(makes)).all()
    ]
    return jsonify(models)
