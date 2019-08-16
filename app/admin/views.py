from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    send_from_directory,
    current_app,
    jsonify,
)

from app.models import *
from app.decorators import admin_required
from flask_login import current_user, login_required
from app.admin.forms import *
from app.auth.forms import *
from flask_rq import get_queue
from app.email import send_email
from app.auth.email import send_confirm_email
from app.auth.email import send_password_reset_email
from app.auth.admin_decorators import check_confirmed
from sqlalchemy import func
from flask_ckeditor import upload_success, upload_fail


admin = Blueprint("admin", __name__)
photos = UploadSet("photos", IMAGES)


@admin.route("/")
@login_required
@admin_required
@check_confirmed
def dashboard():
    """Admin dashboard page."""
    bookings = Booking.query.order_by(Booking.createdAt.desc()).limit(5)
    listings = (
        Listing.query.filter_by(published=True)
        .order_by(Listing.createdAt.desc())
        .limit(5)
    )
    croles = Role.query.filter_by(index="customer").first_or_404()
    customers = croles.users.order_by(User.createdAt.desc()).limit(5)
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).limit(5)
    makes = Make.query.order_by(Make.createdAt.desc()).limit(5)
    models = Model.query.order_by(Model.createdAt.desc()).limit(5)
    bookingsCount = Booking.query.count()
    listingsCount = Listing.query.filter_by(published=True).count()
    customersCount = customers.count()
    vehicles_count = all_vehicles.count()
    makes_count = Make.query.count()
    models_count = Model.query.count()

    return render_template(
        "admin/index.html",
        all_vehicles=all_vehicles,
        vehicles_count=vehicles_count,
        makes_count=makes_count,
        models_count=models_count,
        makes=makes,
        models=models,
    )


@admin.route("/all_vehicles")
@login_required
@admin_required
@check_confirmed
def vehicles():
    """Vehicles."""
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).all()
    return render_template("admin/all_vehicles.html", all_vehicles=all_vehicles)


@admin.route("/vehicle/add", methods=["GET", "POST"])
@login_required
@admin_required
@check_confirmed
def add_vehicle():
    all_vehicles = Vehicle.query.all()
    """Create a new vehicle."""
    form = AddVehicleForm()
    form.make.choices = [(row.id, row.name) for row in Make.query.all()]
    form.model.choices = [(row.id, row.name) for row in Model.query.all()]
    if form.validate_on_submit():
        front_image = form.front_image.data
        if front_image:
            front_image = photos.save(form.front_image.data)

        back_image = form.back_image.data
        if back_image:
            back_image = photos.save(form.back_image.data)

        left_image = form.left_image.data
        if left_image:
            left_image = photos.save(form.left_image.data)

        right_image = form.right_image.data
        if right_image:
            right_image = photos.save(form.right_image.data)

        dash_image = form.dash_image.data
        if dash_image:
            dash_image = photos.save(form.dash_image.data)

        interior_image = form.interior_image.data
        if interior_image:
            interior_image = photos.save(form.interior_image.data)

        make = Make.query.filter_by(id=form.make.data).first_or_404()
        model = Model.query.filter_by(id=form.model.data).first_or_404()
        new_vehicle = Vehicle(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            plate=form.plate.data,
            year=form.year.data,
            image_url=front_image,
            back_image_url=back_image,
            dash_image_url=dash_image,
            front_image_url=front_image,
            interior_image_url=interior_image,
            left_image_url=left_image,
            right_image_url=right_image,
            mileage=form.mileage.data,
            color=form.color.data,
            condition=form.condition.data,
            seller_name=form.seller_name.data,
            seller_email=form.seller_email.data,
            phone_number=form.phone_number.data,
            area=form.area.data,
            model_id=model.id,
            make_id=make.id,
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for("admin.vehicles"))
    return render_template("admin/new_vehicle.html", form=form)


@admin.route("/_get_model")
@login_required
@admin_required
def _get_model():
    make_id = request.args.get("make_id", 0, type=int)
    models = [
        (row.id, row.name) for row in Model.query.filter_by(make_id=make_id).all()
    ]
    return jsonify(models)


@admin.route("/settings", methods=("GET", "POST"))
@login_required
@admin_required
def admin_settings():
    user = current_user

    return render_template("admin/blank.html", user=user)


@admin.route("/settings/change_password", methods=("GET", "POST"))
@login_required
@admin_required
@check_confirmed
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been updated.", "green")
            return redirect(url_for("admin.settings"))
        else:
            flash("Original password is invalid.", "red")
    return render_template("admin/change_password.html", form=form)


@admin.route("/settings/change-email", methods=["GET", "POST"])
@admin_required
@login_required
@check_confirmed
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for(
                "account.change_email", token=token, _external=True
            )
            get_queue().enqueue(
                send_email,
                recipient=new_email,
                subject="Confirm Your New Email",
                template="account/email/change_email",
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user._get_current_object(),
                change_email_link=change_email_link,
            )
            flash(
                "A confirmation link has been sent to {}.".format(new_email), "warning"
            )
            return redirect(url_for("admin.settings"))
        else:
            flash("Invalid email or password.", "form-error")
    return render_template("admin/change_email.html", form=form)


@admin.route("/settings/change-email/<token>", methods=["GET", "POST"])
@login_required
@admin_required
@check_confirmed
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash("Your email address has been updated.", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "error")
    return redirect(url_for("admin.dashboard"))


@admin.route("/category")
@admin_required
@check_confirmed
def category():
    categories = Category.query.order_by(Category.createdAt.desc()).all()
    return render_template("admin/category.html", items=categories)


@admin.route("/category/new", methods=("GET", "POST"))
@admin_required
@check_confirmed
def newCategory():
    form = CategoryForm()
    if form.validate_on_submit():
        image = form.image.data
        if image:
            image = photos.save(form.image.data)
        category = Category(name=form.name.data, image_url=image)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully", "green")
        return redirect(url_for("admin.category"))
    return render_template("admin/add_category.html", form=form)


@admin.route("/files/<path:filename>")
def uploaded_files(filename):
    path = current_app.config["UPLOADS_CKEDITOR"]
    return send_from_directory(path, filename)


@admin.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("upload")
    # Add more validations here
    extension = f.filename.split(".")[1].lower()
    if extension not in ["jpg", "gif", "png", "jpeg"]:
        return upload_fail(message="Image only!")
    f.save(os.path.join("app/static/ckeditor_uploads", f.filename))
    url = url_for("admin.uploaded_files", filename=f.filename)
    return upload_success(url=url)  # return upload_success call
