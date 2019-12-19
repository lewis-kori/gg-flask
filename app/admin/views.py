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
from werkzeug.datastructures import FileStorage


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
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).all()
    makes = Make.query.order_by(Make.createdAt.desc()).limit(5)
    models = Model.query.order_by(Model.createdAt.desc()).limit(5)
    bookingsCount = Booking.query.count()
    listingsCount = Listing.query.filter_by(published=True).count()
    customersCount = customers.count()
    vehicles_count = Vehicle.query.count()
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


@admin.route("/view_vehicle/<id>")
@login_required
@admin_required
@check_confirmed
def view_vehicle(id):
    """View Vehicle."""
    all_vehicles = Vehicle.query.order_by(Vehicle.createdAt.desc()).all()
    vehicle = Vehicle.query.get_or_404(id)
    fuel_id = vehicle.fuel_type_id
    car_fuel_type = Fuel.query.filter_by(id=fuel_id).first_or_404()
    return render_template(
        "admin/view_vehicle.html",
        all_vehicles=all_vehicles,
        vehicle=vehicle,
        fuel_id=fuel_id,
        car_fuel_type=car_fuel_type,
    )


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
    form.transmission.choices = [(row.id, row.type) for row in Transmission.query.all()]
    form.fuel_type.choices = [(row.id, row.type) for row in Fuel.query.all()]
    form.features.choices = [(row.id, row.name) for row in Feature.query.all()]
    if form.validate_on_submit():
        make = Make.query.filter_by(id=form.make.data).first_or_404()
        model = Model.query.filter_by(id=form.model.data).first_or_404()
        transmission = Transmission.query.filter_by(
            id=form.transmission.data
        ).first_or_404()
        fuel = Fuel.query.filter_by(id=form.fuel_type.data).first_or_404()
        new_vehicle = Vehicle(
            name=form.name.data,
            price=form.price.data,
            featured=form.featured.data,
            description=form.description.data,
            plate=form.plate.data,
            year=form.year.data,
            image_url=form.front_image.data,
            back_image_url=form.back_image.data,
            dash_image_url=form.dash_image.data,
            front_image_url=form.front_image.data,
            interior_image_url=form.interior_image.data,
            left_image_url=form.left_image.data,
            right_image_url=form.right_image.data,
            extra_images_url=form.extra_images.data,
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
        for feature_id in form.features.data:
            feature = Feature.query.filter_by(id=feature_id).first_or_404()
            new_vehicle.features.append(feature)
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for("admin.vehicles"))
    return render_template("admin/new_vehicle.html", form=form)


@admin.route("/vehicle/edit/<id>", methods=["GET", "POST"])
@login_required
@admin_required
@check_confirmed
def edit_vehicle(id):
    vehicle = Vehicle.query.filter_by(id=id).first_or_404()

    """Create a new vehicle."""
    form = EditVehicleForm(obj=vehicle)
    form.make_id.choices = [(row.id, row.name) for row in Make.query.all()]
    form.model_id.choices = [(row.id, row.name) for row in Model.query.all()]
    form.transmission_id.choices = [
        (row.id, row.type) for row in Transmission.query.all()
    ]
    form.fuel_type_id.choices = [(row.id, row.type) for row in Fuel.query.all()]
    form.features_id.choices = [(row.id, row.name) for row in Feature.query.all()]

    if form.validate_on_submit():
        form.make = Make.query.filter_by(id=form.make_id.data).first_or_404()
        form.model = Model.query.filter_by(id=form.model_id.data).first_or_404()
        form.transmission = Transmission.query.filter_by(
            id=form.transmission_id.data
        ).first_or_404()
        form.fuel = Fuel.query.filter_by(id=form.fuel_type_id.data).first_or_404()
        form.image_url = (form.front_image_url.data,)
        form.back_image_url = (form.back_image_url.data,)
        form.dash_image_url = (form.dash_image_url.data,)
        form.front_image_url = (form.front_image_url.data,)
        form.interior_image_url = (form.interior_image_url.data,)
        form.extra_images_url = (form.extra_images.data,)
        form.left_image_url = (form.left_image_url.data,)
        form.right_image_url = (form.right_image_url.data,)
        for form.feature_id in form.features_id.data:
            form.feature = Feature.query.filter_by(id=form.feature_id).first_or_404()
            vehicle.features_id.append(form.feature)

        form.populate_obj(vehicle)
        db.session.commit()
        return redirect(url_for("admin.view_vehicle", id=id))
    return render_template("admin/edit_vehicle.html", form=form, vehicle=vehicle)


@admin.route("/_get_model")
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
    form = ChangeUserEmailForm()
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
    f = request.files.get("file")
    # Add more validations here
    extension = f.filename.split(".")[1].lower()
    if extension not in ["jpg", "gif", "png", "jpeg"]:
        return upload_fail(message="Image only!")
    f.save(os.path.join("app/static/ckeditor_uploads", f.filename))
    url = url_for("admin.uploaded_files", filename=f.filename)
    return upload_success(url=url)  # return upload_success call


@admin.route("/view_vehicle/<id>/delete")
@login_required
@admin_required
@check_confirmed
def delete_vehicle(id):
    """View Vehicle."""
    vehicle = Vehicle.query.get_or_404(id)

    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for("admin.vehicles"))


# @admin.route('/reserved_cars', methods=['GET', 'POST'])
# @login_required
# @admin_required
# @check_confirmed
# def reserved_cars():
#     g.search_form.table.data = 'Inventory'
#     page = request.args.get('page', 1, type=int)
#     inventory = Vehicle.query.filter_by(state='reserved').order_by(Vehicle.created_at.desc()).paginate(page,
#                                                                                                        current_app.config[
#                                                                                                            'POSTS_PER_PAGE'],
#                                                                                                        False)
#     next_url = url_for('admin.inventory', page=inventory.next_num) if inventory.has_next else None
#     prev_url = url_for('admin.inventory', page=inventory.prev_num) if inventory.has_prev else None
#     return render_template('admin/inventory.html', inventory=inventory.items, next_url=next_url, prev_url=prev_url,
#                            title='inventory')


@admin.route('/enquiry', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def enquiry():
    enquiry = Enquiry.query.order_by(Enquiry.created_at.desc()).all()
    return render_template('admin/enquiries.html', enquiries=enquiry, title='Enquiry')


@admin.route('/bazaar', methods=['GET', 'POST'])
@admin_required
@check_confirmed
@login_required
def bazaar():
    bazaar = Bazaar.query.order_by(Bazaar.created_at.desc()).all()
    return render_template('admin/bazaar.html', bazaars=bazaar, title='Bazaar')


@admin.route('/create_bazaar', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def create_bazaar():
    form = BazaarForm()
    if form.validate_on_submit():
        bazaar = Bazaar(name=form.name.data, location=form.location.data, phone=form.phone.data,
                        color=str(form.color.data))
        db.session.add(bazaar)
        db.session.commit()
        flash('Bazaar added successfully', 'success')
        return redirect(url_for('admin.bazaar'))
    return render_template('admin/create_bazaar.html', form=form, title='Create Bazaar')


@admin.route('/add_bazaar/<id>', methods=['POST'])
@login_required
def add_bazaar(id):
    form = AddBazaarForm()
    form.bazaar.choices = [(row.id, row.name) for row in Bazaar.query.order_by(Bazaar.created_at.desc()).all()]
    if form.validate_on_submit():
        vehicle = Vehicle.query.filter_by(id=id).first_or_404()
        bazaar = Bazaar.query.filter_by(id=form.bazaar.data).first_or_404()
        vehicle.bazaar = bazaar
        db.session.commit()
        return jsonify({'status': 1, 'message': 'bazaar updated successfully'})
    return jsonify(data=form.errors)


@admin.route('/edit_bazaar/<id>', methods=['GET', 'POST'])
@login_required
def edit_bazaar(id):
    bazaar = Bazaar.query.filter_by(id=id).first_or_404()
    form = BazaarForm(obj=bazaar)
    if form.validate_on_submit():
        bazaar.color = str(form.color.data)
        bazaar.name = form.name.data
        bazaar.location = form.location.data
        bazaar.phone = form.phone.data
        db.session.commit()
        flash('Bazaar edited ', 'success')
        return redirect(url_for('admin.bazaar'))
    return render_template('admin/create_bazaar.html', form=form, title='edit Bazaar')


@admin.route('/view_bazaar/<id>', methods=['GET', 'POST'])
@login_required
def view_bazaar(id):
    page = request.args.get('page', 1, type=int)
    vehicle = Vehicle.query.filter_by(bazaar_id=id).order_by(Vehicle.createdAt.desc()).paginate(page,
                                                                                                 current_app.config[
                                                                                                     'POSTS_PER_PAGE'],
                                                                                                 False)
    next_url = url_for('admin.view_bazaar', id=id, page=vehicle.next_num) if vehicle.has_next else None
    prev_url = url_for('admin.view_bazaar', id=id, page=vehicle.prev_num) if vehicle.has_prev else None
    return render_template('admin/all_vehicles.html', inventory=vehicle.items, next_url=next_url, prev_url=prev_url,
                           title='inventory')


@admin.route('/imports', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def imports():
    imports = Import.query.order_by(Import.created_at.desc()).all()
    return render_template('admin/import.html', imports=imports, title='Imports')


@admin.route('/create_enquiry', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def create_enquiry():
    form = EnquiryForm()
    form.client_id.choices = [(row.id, row.client_name) for row in
                              Client.query.order_by(Client.created_at.desc()).all()]
    form.make.choices = [(row.id, row.name) for row in Make.query.all()]
    form.model.choices = [(row.id, row.name) for row in Model.query.all()]

    if form.validate_on_submit():
        make = Make.query.filter_by(id=form.make.data).first_or_404()
        model = Model.query.filter_by(id=form.model.data).first_or_404()
        client = Client.query.filter_by(id=form.client_id.data).first_or_404()
        vehicle=Vehicle.query.filter_by(make_id=make.id, model_id=model.id).first_or_404()
        enquiry = Enquiry(vehicle=vehicle, client=client,
                          budget=form.budget.data,
                          year=form.year.data)
        db.session.add(enquiry)
        db.session.commit()
        flash('Enquiry added successfully', 'success')
        return redirect(url_for('admin.enquiry'))
    return render_template('admin/create_enquiry.html', form=form, title='create enquiry')

@admin.route('/edit_enquiry/<id>', methods=['GET', 'POST'])
@login_required
def edit_enquiry(id):
    enquiry = Enquiry.query.filter_by(id=id).first_or_404()
    form = EnquiryForm(obj=enquiry)
    form.client_id.choices = [(row.id, row.client_name) for row in
                              Client.query.order_by(Client.created_at.desc()).all()]
    form.make.choices = [(row.id, row.name) for row in Make.query.all()]
    form.model.choices = [(row.id, row.name) for row in Model.query.all()]
    if form.validate_on_submit():
        form.populate_obj(enquiry)
        db.session.commit()
        flash('Enquiry edited ', 'success')
        return redirect(url_for('admin.enquiry'))
    return render_template('admin/edit_enquiry.html', form=form, title='edit enquiry')


@admin.route('/create_import', methods=['GET', 'POST'])
@login_required
@admin_required
@check_confirmed
def create_import():
    form = ImportForm()
    form.client_id.choices = [(row.id, row.client_name) for row in
                              Client.query.order_by(Client.created_at.desc()).all()]
    form.make.choices = [(row.id, row.name) for row in Make.query.all()]
    form.model.choices = [(row.id, row.name) for row in Model.query.all()]
    form.transmission.choices = [(row.id, row.type) for row in Transmission.query.all()]
    form.fuel_type.choices = [(row.id, row.type) for row in Fuel.query.all()]
    if form.validate_on_submit():
        client = Client.query.filter_by(id=form.client_id.data).first_or_404()
        vehicle = Vehicle.query.filter_by(make=form.make.data, model=form.model.data).first_or_404()
        transmission = Transmission.query.filter_by(
            id=form.transmission.data
        ).first_or_404()
        fuel = Fuel.query.filter_by(id=form.fuel_type.data).first_or_404()
        import_car = Import(vehicle=vehicle, client=client, budget=form.budget.data, year=form.year.data,
                            color=form.color.data, fuel=fuel, transmission=transmission,
                            engine=form.engine.data, special_features=form.special_features.data)
        db.session.add(import_car)
        db.session.commit()
        flash('Import added successfully', 'success')
        return redirect(url_for('admin.imports'))
    return render_template('admin/create_import.html', form=form, title='Add import')


@admin.route('/edit_import/<id>', methods=['GET', 'POST'])
@login_required
def edit_import(id):
    import_car = Import.query.filter_by(id=id).first_or_404()
    form = ImportForm(obj=import_car)
    form.client_id.choices = [(row.id, row.client_name) for row in
                              Client.query.order_by(Client.created_at.desc()).all()]
    form.make.choices = [(row.id, row.name) for row in Make.query.all()]
    form.model.choices = [(row.id, row.name) for row in Model.query.all()]
    if form.validate_on_submit():
        form.populate_obj(import_car)
        db.session.commit()
        flash('Import edited ', 'success')
        return redirect(url_for('admin.imports'))
    return render_template('admin/edit_import.html', form=form, title='edit import')

##finance starts here
# invoice
@admin.route('/invoices')
@login_required
def invoices():
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return render_template('admin/invoices.html', title='Invoice', invoices=invoices)


# quotations
@admin.route('/quotations')
@login_required
def quotations():
    quotations = Quotation.query.order_by(Quotation.created_at.desc()).all()
    return render_template('admin/quotations.html', title='Quotations', quotations=quotations)


# bills
@admin.route('/bills')
@login_required
def bills():
    bills = Bill.query.order_by(Bill.created_at.desc()).all()
    return render_template('admin/bills.html', title='Bill', bills=bills)


# payments
@admin.route('/payments')
@login_required
def payments():
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('admin/payments.html', title='Payment', payments=payments)


# trade_in
@admin.route('/trade_in')
@login_required
def trade_in():
    requests = Tradein.query.order_by(Tradein.created_at.desc()).all()
    return render_template('admin/trade_in.html', title='Trade-in', requests=requests)


# import
@admin.route('/import_requests')
@login_required
def import_requests():
    requests = Import.query.order_by(Import.created_at.desc()).all()
    return render_template('admin/import_requests.html', title='Import requests', requests=requests)


# Clients
@admin.route('/clients', methods=['GET', 'POST'])
@login_required
def clients():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(client_name=form.client_name.data, client_type=form.client_type.data,
                        phone_number=form.phone_number.data, email=form.email.data, location=form.location.data)
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully', 'success')
        return redirect(url_for('admin.clients'))
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template('admin/clients.html', title='clients', form=form, clients=clients)


# suppliers
@admin.route('/suppliers', methods=['GET', 'POST'])
@login_required
def suppliers():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(supplier_name=form.supplier_name.data, supplier_type=form.supplier_type.data,
                            phone_number=form.phone_number.data, email=form.email.data,
                            location=form.location.data, bank_name=form.bank_name.data,
                            bank_country=form.bank_country.data,
                            bank_address=form.bank_address.data, account_number=form.account_number.data)
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully', 'success')
        return redirect(url_for('admin.suppliers'))
    suppliers = Supplier.query.order_by(Supplier.created_at.desc()).all()
    return render_template('admin/suppliers.html', title='suppliers', form=form, suppliers=suppliers)


# create quotation
@admin.route('/create_quotation', methods=['GET', 'POST'])
@login_required
def create_quotation():
    form = QuotationForm()
    form.client_id.choices = [(row.id, row.client_name) for row in
                              Client.query.order_by(Client.created_at.desc()).all()]
    if form.validate_on_submit():
        quotation_number = 'QUO-001'
        quotation = Quotation.query.order_by(Quotation.created_at.desc()).first()
        if quotation is not None:
            quot_no = quotation.quotation_no.strip('QUO-')
            no = 1
            quotation_no = int(quot_no) + int(no)
            quotation_number = "QUO-00" + str(quotation_no)
        client = Client.query.filter_by(id=form.client_id.data).first_or_404()
        quotation = Quotation(quotation_name=form.quotation_name.data, quotation_no=quotation_number,
                              quotation_date=form.quotation_date.data,
                              description=form.description.data, amount=form.amount.data, client=client)
        db.session.add(quotation)
        db.session.commit()
        quotation_id = Quotation.query.order_by(Quotation.created_at.desc()).first()
        for item in form.products.data:
            products = Product(product=item['product'], price=item['price'], quantity=item['quantity'],
                               size=item['size'], total=item['total'], quotation=quotation_id)
            db.session.add(products)
            db.session.commit()
        flash('Quotation added successfully', 'success')
        return redirect(url_for('admin.quotations'))

    return render_template('admin/create_quotation.html', title="create Quotation", form=form)


# create invoice
@admin.route('/create_invoice', methods=['POST'])
@login_required
def create_invoice():
    invoice_number = 'INV-001'
    invoice = Invoice.query.order_by(Invoice.created_at.desc()).first()
    if invoice is not None:
        inv_no = invoice.invoice_no.strip('INV-')
        no = 1
        invoice_no = int(inv_no) + int(no)
        invoice_number = "INV-00" + str(invoice_no)
    id = request.form['id']
    date_due = request.form['due_date']
    date = datetime.strptime(date_due, '%Y-%m-%d')
    due_date = datetime.combine(date, datetime.min.time())
    quotation = Quotation.query.filter_by(id=id).first_or_404()
    save_invoice = Invoice(invoice_no=invoice_number, date_due=due_date, quotation=quotation)
    db.session.add(save_invoice)
    db.session.commit()
    invoice = Invoice.query.order_by(Invoice.created_at.desc()).first_or_404()
    return jsonify({'status': 1, 'id': invoice.id})


# create bill
@admin.route('/create_bill', methods=['GET', 'POST'])
@login_required
def create_bill():
    form = BillForm()
    form.supplier_id.choices = [(row.id, row.supplier_name) for row in
                                Supplier.query.order_by(Supplier.created_at.desc()).all()]

    if form.validate_on_submit():

        bill_number = 'BIL-001'
        bill = Bill.query.order_by(Bill.created_at.desc()).first()
        if bill is not None:
            bi_no = bill.bill_no.strip('BIL-')
            no = 1
            bill_no = int(bi_no) + int(no)
            bill_number = "BIL-00" + str(bill_no)
        supplier = Supplier.query.filter_by(id=form.supplier_id.data).first_or_404()
        bill = Bill(bill_name=form.bill_name.data, bill_no=bill_number, date_due=form.date_due.data,
                    description=form.description.data, amount=form.amount.data, supplier=supplier)
        db.session.add(bill)
        db.session.commit()
        flash('Bill added successfully', 'success')
        return redirect(url_for('admin.bills'))
    return render_template('admin/create_bill.html', title="create Bill", form=form)


# create payment
@admin.route('/create_payment', methods=['GET', 'POST'])
@login_required
def create_payment():
    form = PaymentForm()
    form.invoice_id.choices = [(row.id, row.quotation.quotation_name) for row in
                               Invoice.query.order_by(Invoice.created_at.desc()).all()]

    if form.validate_on_submit():
        invoice = Invoice.query.filter_by(id=form.invoice_id.data).first_or_404()
        payment = Payment(payment_mode=form.payment_mode.data, payment_type=form.payment_type.data,
                          note=form.note.data, amount=form.amount.data, invoice=invoice)
        db.session.add(payment)
        db.session.commit()
        flash('Payment added successfully', 'success')
        return redirect(url_for('admin.payments'))
    return render_template('admin/create_payment.html', title="create Payment", form=form)


# edit quotation
@admin.route('/edit_quotation/<id>', methods=['GET', 'POST'])
@login_required
def edit_quotation(id):
    quotation = Quotation.query.filter_by(id=id).first_or_404()
    form = EditQuotationForm(obj=quotation)
    form.client_id.choices = [(row.id, row.client_name) for row in
                              Client.query.order_by(Client.created_at.desc()).all()]
    if form.validate_on_submit():
        form.populate_obj(quotation)
        db.session.commit()
        flash('Quotation edited successfully', 'success')
        return redirect(url_for('admin.quotations'))
    return render_template('admin/edit_quotation.html', form=form)


# edit bill
@admin.route('/edit_bill/<id>', methods=['GET', 'POST'])
@login_required
def edit_bill(id):
    bill = Bill.query.filter_by(id=id).first_or_404()
    form = BillForm(obj=bill)
    form.supplier_id.choices = [(row.id, row.supplier_name) for row in
                                Supplier.query.order_by(Supplier.created_at.desc()).all()]

    if form.validate_on_submit():
        form.populate_obj(bill)
        db.session.commit()
        flash('Bill edited successfully', 'success')
        return redirect(url_for('admin.bills'))

    return render_template('admin/edit_bill.html', form=form, title='Edit Bill')


# edit payment
@admin.route('/edit_payment/<id>', methods=['GET', 'POST'])
@login_required
def edit_payment(id):
    payment = Payment.query.filter_by(id=id).first_or_404()
    form = PaymentForm(obj=payment)
    form.invoice_id.choices = [(row.id, row.quotation.quotation_name) for row in
                               Invoice.query.order_by(Invoice.created_at.desc()).all()]
    if form.validate_on_submit():
        form.populate_obj(payment)
        db.session.commit()
        flash('Payment edited successfully', 'success')
        return redirect(url_for('admin.payments'))
    return render_template('admin/edit_payment.html', form=form, title='Edit Payment')


# edit client
@admin.route('/edit_client/<id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    client = Client.query.filter_by(id=id).first_or_404()
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        form.populate_obj(client)
        db.session.commit()
        flash('Client edited successfully', 'success')
        return redirect(url_for('admin.clients'))
    elif request.method == 'GET':
        data = {'client_type': client.client_type, 'client_name': client.client_name,
                'phone_number': client.phone_number, 'email': client.email, 'location': client.location}
        return jsonify({'status': 1, 'data': data})


# edit supplier
@admin.route('/edit_supplier/<id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.filter_by(id=id).first_or_404()
    form = SupplierForm(obj=supplier)
    if form.validate_on_submit():
        form.populate_obj(supplier)
        db.session.commit()
        flash('Supplier edited successfully', 'success')
        return redirect(url_for('admin.suppliers'))
    elif request.method == 'GET':
        data = {'supplier_type': supplier.supplier_type, 'supplier_name': supplier.supplier_name,
                'phone_number': supplier.phone_number, 'email': supplier.email,
                'location': supplier.location, 'bank_name': supplier.bank_name, 'bank_country': supplier.bank_country,
                'bank_address': supplier.bank_address, 'account_number': supplier.account_number}
        return jsonify({'status': 1, 'data': data})


# view invoice
@admin.route('/view_invoice/<id>')
@login_required
def view_invoice(id):
    invoice = Invoice.query.filter_by(id=id).first_or_404()
    return render_template('admin/view_invoice.html', title='view invoice', invoice=invoice)


# view quotation
@admin.route('/view_quotation/<id>')
@login_required
def view_quotation(id):
    quotation = Quotation.query.filter_by(id=id).first_or_404()
    return render_template('admin/view_quotation.html', title='view quotation', quotation=quotation)


# view bill
@admin.route('/view_bill/<id>')
@login_required
def view_bill(id):
    bill = Bill.query.filter_by(id=id).first_or_404()
    return render_template('admin/view_bill.html', title='view bill', bill=bill)


# view payment
@admin.route('/view_payment/<id>')
@login_required
def view_payment(id):
    payment = Payment.query.filter_by(id=id).first_or_404()
    return render_template('admin/view_payment.html', title='view payment', payment=payment)


# view clients
@admin.route('/view_client/<id>')
@login_required
def view_client(id):
    client = Client.query.filter_by(id=id).first_or_404()
    return render_template('admin/view_client.html', title='view client', client=client)


# view suppliers
@admin.route('/view_supplier/<id>')
@login_required
def view_supplier(id):
    supplier = Supplier.query.filter_by(id=id).first_or_404()
    return render_template('admin/view_supplier.html', title='view supplier', supplier=supplier)
##endfinance


@admin.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    id = request.form['id']
    tablename = request.form['table']
    if tablename == 'Client':
        table = Client.query.filter_by(id=id).first_or_404()
    elif tablename == 'Quotation':
        table = Quotation.query.filter_by(id=id).first_or_404()
    elif tablename == 'Invoice':
        table = Invoice.query.filter_by(id=id).first_or_404()
    elif tablename == 'Payment':
        table = Payment.query.filter_by(id=id).first_or_404()
    elif tablename == 'Supplier':
        table = Supplier.query.filter_by(id=id).first_or_404()
    elif tablename == 'Bill':
        table = Bill.query.filter_by(id=id).first_or_404()
    elif tablename == 'Enquiry':
        table = Enquiry.query.filter_by(id=id).first_or_404()
    elif tablename == 'Import':
        table = Import.query.filter_by(id=id).first_or_404()
    elif tablename == 'Tradein':
        table = Tradein.query.filter_by(id=id).first_or_404()
    elif tablename == 'Import':
        table = Import.query.filter_by(id=id).first_or_404()
    elif tablename == 'Vehicle':
        table = Vehicle.query.filter_by(id=id).first_or_404()
    elif tablename == 'User':
        table = User.query.filter_by(id=id).first_or_404()
        if table.status == True:
            return jsonify({'status': 0,'message':'User must be deactivated first'})
        if table.id == 1:
            return jsonify({'status': 0,'message':'Cannot delete superadmin'})
    elif tablename == 'Role':
            table = Role.query.filter_by(id=id).first_or_404()
    elif tablename == 'Bazaar':
            table = Bazaar.query.filter_by(id=id).first_or_404()
    db.session.delete(table)
    db.session.commit()
    return jsonify({'status': 1})


@admin.route('/delete_carpic', methods=['GET', 'POST'])
@login_required
def delete_carpic():
    return


@admin.route("/sellers_vehicles")
@login_required
@admin_required
@check_confirmed
def sellers_vehicles():
    """Sellers Vehicles."""
    sellers_vehicles = SellersVehicle.query.order_by(SellersVehicle.createdAt.desc())\
        .join(Make, Model).all()

    return render_template("admin/sellers_vehicles.html", sellers_vehicles=sellers_vehicles)


@admin.route("/importers_vehicles")
@login_required
@admin_required
@check_confirmed
def importers_vehicles():
    """Importers Vehicles."""
    all_imports = Import.query.order_by(Import.createdAt.desc()).all()
    return render_template("admin/importers_vehicles.html", all_imports=all_imports)


@admin.route("/contact_us_backend")
@login_required
@admin_required
@check_confirmed
def contact_us_backend():
    """CONTACT US."""
    all_questions = Contact.query.all()
    return render_template("admin/contact_us_backend.html", all_questions=all_questions)
