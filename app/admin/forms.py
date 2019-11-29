from flask_wtf import Form, FlaskForm
from wtforms import ValidationError
from flask_ckeditor import CKEditorField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import Form as NoCsrfForm
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    TextAreaField,
    FileField,
    FormField,
    HiddenField,
    SelectMultipleField,
    BooleanField,
    IntegerField,
    DecimalField,
)
from wtforms.fields import BooleanField, StringField, SubmitField, FloatField, PasswordField, IntegerField, DateField, \
    SelectField, FieldList, TextAreaField, FormField, HiddenField, DecimalField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, DataRequired
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import db
from app.models import Role, User, Category, Product

photos = UploadSet("photos", IMAGES)


class ChangeUserEmailForm(Form):
    email = EmailField(
        "New email", validators=[InputRequired(), Length(1, 64), Email()]
    )
    submit = SubmitField("Update email")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")


class ChangeAccountTypeForm(Form):
    role = QuerySelectField(
        "New account type",
        validators=[InputRequired()],
        get_label="name",
        query_factory=lambda: db.session.query(Role).order_by("permissions"),
    )
    submit = SubmitField("Update role")


class InviteUserForm(Form):
    first_name = StringField("First name", validators=[InputRequired(), Length(1, 64)])
    last_name = StringField("Last name", validators=[InputRequired(), Length(1, 64)])
    email = EmailField("Email", validators=[InputRequired(), Length(1, 64), Email()])
    submit = SubmitField("Invite")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")


class NewUserForm(InviteUserForm):
    password = PasswordField("Password", validators=[InputRequired()])
    password2 = PasswordField(
        "Confirm password",
        validators=[InputRequired(), EqualTo("password", "Passwords must match.")],
    )

    submit = SubmitField("Create")


class AddMakeForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(1, 64)])
    image = FileField(validators=[FileAllowed(photos, u"Image only!")])
    description = CKEditorField("Description")
    submit = SubmitField("Add")


class EditMakeForm(Form):
    name = StringField("Name", validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField(
        "Description", validators=[InputRequired(), Length(1, 64)]
    )
    image_url = FileField(validators=[FileAllowed(photos, u"Image only!")])
    submit = SubmitField("Add")


class AddVehicleForm(FlaskForm):
    plate = StringField("Plate")
    featured = BooleanField("Featured")
    description = TextAreaField("Description", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    mileage = StringField("Mileage", validators=[InputRequired()])
    color = StringField("Color", validators=[InputRequired()])
    condition = StringField("Condition")
    year = IntegerField("Year", validators=[InputRequired()])
    model = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    make = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    fuel_type = SelectField(choices=[], coerce=int)
    transmission = SelectField(choices=[], coerce=int)
    interior = StringField("Interior")
    engine_size = StringField("Engine Size")
    features = SelectMultipleField(choices=[], coerce=int)
    front_image = StringField(validators=[InputRequired()])
    back_image = StringField()
    left_image = StringField()
    right_image = StringField()
    dash_image = StringField()
    interior_image = StringField()
    extra_images = StringField()
    seller_email = StringField("Email", validators=[InputRequired()])
    seller_name = StringField("Name", validators=[InputRequired()])
    phone_number = StringField("Phone", validators=[InputRequired()])
    area = StringField("Area", validators=[InputRequired()])
    submit = SubmitField("Add")


class AddVehicleImagesForm(FlaskForm):
    front_image = FileField(
        validators=[FileAllowed(photos, u"Image only!"), FileRequired()]
    )
    back_image = FileField(validators=[FileAllowed(photos, u"Image only!")])
    left_image = FileField(validators=[FileAllowed(photos, u"Image only!")])
    right_image = FileField(validators=[FileAllowed(photos, u"Image only!")])
    dash_image = FileField(validators=[FileAllowed(photos, u"Image only!")])
    interior_image = FileField(validators=[FileAllowed(photos, u"Image only!")])
    submit = SubmitField("Add")


class GiantForm(FlaskForm):
    part_one = FormField(AddVehicleForm)
    part_two = FormField(AddVehicleImagesForm)


class EditVehicleForm(Form):
    plate = StringField("Plate")
    featured = BooleanField("Featured")
    description = TextAreaField("Description", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    mileage = StringField("Mileage", validators=[InputRequired()])
    color = StringField("Color", validators=[InputRequired()])
    condition = StringField("Condition")
    year = IntegerField("Year", validators=[InputRequired()])
    model_id = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    make_id = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    fuel_type_id = SelectField(choices=[], coerce=int)
    transmission_id = SelectField(choices=[], coerce=int)
    interior = StringField("Interior")
    engine_size = StringField("Engine Size")
    features_id = SelectMultipleField(choices=[], coerce=int)
    front_image_url = StringField()
    back_image_url = StringField()
    left_image_url = StringField()
    right_image_url = StringField()
    dash_image_url = StringField()
    interior_image_url = StringField()
    extra_images = StringField()
    seller_email = StringField("Email", validators=[InputRequired()])
    seller_name = StringField("Name", validators=[InputRequired()])
    phone_number = StringField("Phone", validators=[InputRequired()])
    area = StringField("Area", validators=[InputRequired()])
    submit = SubmitField("Edit")


class AddModelForm(Form):
    name = StringField("Name", validators=[InputRequired(), Length(1, 64)])
    description = CKEditorField("Description")
    image_url = FileField(validators=[FileAllowed(photos, u"Image only!")])
    make_id = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    submit = SubmitField("Add")


class EditModelForm(Form):
    name = StringField("Name", validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField(
        "Description", validators=[InputRequired(), Length(1, 64)]
    )
    image_url = FileField(validators=[FileAllowed(photos, u"Image only!")])
    make_id = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    submit = SubmitField("Add")


class CategoryForm(Form):
    name = StringField("name", validators=[Length(min=2, max=80)])
    image = FileField(validators=[FileAllowed(photos, u"Image only!")])
    submit = SubmitField("save")

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category is not None:
            raise ValidationError("This category has already been added")


class AddBazaarForm(FlaskForm):
    bazaar = SelectField(validators=[DataRequired()], coerce=int)


class ClientForm(FlaskForm):
    client_name = StringField('client name', validators=[DataRequired()])
    client_type = StringField('client type', validators=[DataRequired()])
    phone_number = IntegerField('phone number', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    location = StringField('location', validators=[DataRequired()])
    submit = SubmitField('save')


class ProductForm(NoCsrfForm):
    product = StringField('product', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    size = IntegerField('size', validators=[DataRequired()])
    total = IntegerField('total', validators=[DataRequired()])


class QuotationForm(FlaskForm):
    client_id = SelectField('client_id', coerce=int, id='select_client')
    quotation_name = StringField('quotation_name', validators=[DataRequired()])
    quotation_date = DateField('quotation_date', format='%d/%m/%Y')
    products = FieldList(FormField(ProductForm), min_entries=1)
    amount = IntegerField('amount', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    submit = SubmitField('save')


class EditQuotationForm(FlaskForm):
    client_id = SelectField('client_id', coerce=int, id='select_client')
    quotation_name = StringField('quotation_name', validators=[DataRequired()])
    quotation_date = DateField('quotation_date', format='%d/%m/%Y')
    products = FieldList(FormField(ProductForm, default=lambda: Product()), min_entries=1)
    amount = IntegerField('amount', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    submit = SubmitField('save')


class PaymentForm(FlaskForm):
    invoice_id = SelectField('invoice_id', validators=[DataRequired()], coerce=int, id='select_invoice')
    payment_mode = SelectField('payment_mode', validators=[DataRequired()],
                               choices=[('cash', 'cash'), ('cheque', 'cheque'), ('online-payment', 'online payment')])
    payment_type = StringField('payment_type', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[DataRequired()])
    note = TextAreaField('note', validators=[DataRequired()])
    submit = SubmitField('save')


class SupplierForm(FlaskForm):
    supplier_name = StringField('supplier name name', validators=[DataRequired()])
    supplier_type = StringField('supplier type', validators=[DataRequired()])
    phone_number = IntegerField('phone number', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    location = StringField('location', validators=[DataRequired()])
    bank_name = StringField('bank_name', validators=[DataRequired()])
    bank_country = StringField('bank_country', validators=[DataRequired()])
    bank_address = StringField('bank_address', validators=[DataRequired()])
    account_number = IntegerField('account_number', validators=[DataRequired()])
    submit = SubmitField('save')


class BillForm(FlaskForm):
    supplier_id = SelectField('supplier_id', coerce=int, id='select_supplier')
    bill_name = StringField('bill_name', validators=[DataRequired()])
    date_due = DateField('date_due', format='%d/%m/%Y')
    amount = IntegerField('amount', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    submit = SubmitField('save')


class EnquiryForm(FlaskForm):
    client_id = SelectField('client_id', coerce=int, id='select_client')
    year = StringField('year', validators=[DataRequired()])
    make = SelectField(validators=[DataRequired()], id="car-makes")
    model = SelectField(validators=[DataRequired()], id="car-models")
    budget = DecimalField(validators=[DataRequired()])
    submit = SubmitField('save')


class BazaarForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    phone = StringField('location', validators=[DataRequired()])
    color = StringField(validators=[DataRequired()])
    submit = SubmitField('Save')


class ImportForm(FlaskForm):
    client_id = SelectField('client_id', coerce=int, id='select_client')
    year = SelectField(validators=[DataRequired()], coerce=int, id="car-years")
    make = SelectField(validators=[DataRequired()], id="car-makes")
    model = SelectField(validators=[DataRequired()], id="car-models")
    color = SelectField(validators=[DataRequired()],
                        choices=[('black', 'Black'), ('white', 'White'), ('blue', 'Blue'), ('red', 'Red'),
                                 ('brown', 'Brown'), ('silver', 'Silver'), ('pearl', 'Pearl'), ('orange', 'Orange'),
                                 ('purple', 'Purple'), ('green', 'Green'), ('red-wine', 'Red-wine'), ('grey', 'Grey'),
                                 ('gold', 'Gold'), ('pink', 'Pink')])
    fuel = SelectField(validators=[DataRequired()], choices=[('petrol', 'Petrol'), ('diesel', 'diesel')])
    transmission = SelectField(validators=[DataRequired()], choices=[('automatic', 'Automatic'), ('manual', 'Manual')])
    budget = DecimalField(validators=[DataRequired()])
    engine = StringField(validators=[DataRequired()])
    special_features = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('save')
