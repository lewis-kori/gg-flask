from flask import url_for
from flask_wtf import Form, FlaskForm
from wtforms import ValidationError
from flask_ckeditor import CKEditorField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import TextAreaField, SelectMultipleField
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    DateField,
    DecimalField,
    SelectField,
    HiddenField,
    IntegerField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length, DataRequired

from app.models import User
from app.models import *


class SearchForm(Form):
    year_from = SelectField(id="car-years_from", coerce=int)
    year_to = SelectField(id="car-years_to", coerce=int)
    make = SelectField(id="car-makes", coerce=int)
    model = SelectField(id="car-models", coerce=int)
    transmission = SelectField(choices=[], id="car-trans", coerce=int)
    fuel = SelectField(choices=[], id="car-fuel", coerce=int)
    submit = SubmitField("FIND A CAR")

    def __init__(self, *args, **kwargs):
        if "formdata" not in kwargs:
            kwargs["formdata"] = request.args
        if "csrf_enabled" not in kwargs:
            kwargs["csrf_enabled"] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class BookingForm(Form):
    departure_date = DateField(
        "Check In", validators=[DataRequired()], format="%m/%d/%Y"
    )
    kids = IntegerField("Kids", validators=[DataRequired()])
    total = HiddenField(validators=[DataRequired()])
    adults = IntegerField("Adults", validators=[DataRequired()])
    book = SubmitField("BOOK NOW")


class PaymentForm(Form):
    email = StringField("Email", validators=[DataRequired()])
    card_holder_name = StringField("Card Holder Name", validators=[DataRequired()])
    card_number = StringField("Card Number", validators=[DataRequired()])
    select_card = SelectField(
        "Select Card",
        validators=[DataRequired()],
        choices=[
            ("1", "EUR 6524 1254 6212 2541"),
            ("2", "EUR 6524 1254 6212 2541"),
            ("3", "USD 1254 6524 2541 6212"),
        ],
    )
    month = SelectField(
        validators=[DataRequired()],
        choices=[
            ("jan", "January"),
            ("feb", "February"),
            ("mar", "March"),
            ("apri", "April"),
            ("may", "May"),
            ("jun", "June"),
            ("jul", "July"),
            ("aug", "August"),
            ("sep", "September"),
            ("octo", "October"),
            ("nov", "November"),
            ("dec", "December"),
        ],
    )
    years = SelectField(
        validators=[DataRequired()],
        choices=[
            ("2018", "2018"),
            ("2019", "2019"),
            ("2020", "2020"),
            ("2021", "2021"),
            ("2022", "2022"),
        ],
    )

    # card_identification_number =  StringField('Card Identification Number', validators=[DataRequired()])
    billing_zip_code = StringField("Billing Zip Code", validators=[DataRequired()])

    confirm_booking = SubmitField("Confirm Booking")


class SellVehicleForm(FlaskForm):
    plate = StringField("Plate")
    description = TextAreaField("Description")
    name = StringField("Name")
    price = StringField("Price", validators=[InputRequired()])
    mileage = StringField("Mileage", validators=[InputRequired()])
    color = StringField("Color", validators=[InputRequired()])
    condition = StringField("Condition")
    year = StringField("Year", validators=[InputRequired()])
    model = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    make = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    fuel_type = SelectField(choices=[], coerce=int)
    transmission = SelectField(choices=[], coerce=int)
    interior = StringField("Interior")
    engine_size = StringField("Engine Size")
    seller_email = StringField("Email", validators=[InputRequired()])
    seller_name = StringField("Name", validators=[InputRequired()])
    phone_number = StringField("Phone", validators=[InputRequired()])
    area = StringField("Area", validators=[InputRequired()])
    submit = SubmitField("Submit")


class ImportVehicleForm(FlaskForm):
    plate = StringField("Plate")
    description = TextAreaField("Description")
    name = StringField("Name")
    price = StringField("Price")
    mileage = StringField("Mileage")
    color = StringField("Color")
    condition = StringField("Condition")
    year = StringField("Year")
    model = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    make = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    fuel_type = SelectField(choices=[], coerce=int)
    transmission = SelectField(choices=[], coerce=int)
    interior = StringField("Interior")
    engine_size = StringField("Engine Size")
    importer_email = StringField("Email", validators=[InputRequired()])
    importer_name = StringField("Name", validators=[InputRequired()])
    phone_number = StringField("Phone", validators=[InputRequired()])
    area = StringField("Area")
    submit = SubmitField("Submit")


class ContactForm(FlaskForm):
    message = TextAreaField("message")
    email = StringField("Email", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    phone_number = StringField("Phone", validators=[InputRequired()])
    subject = StringField("Subject")
    submit = SubmitField("Send Message")


class EnquiryForm(FlaskForm):
    message = TextAreaField("message")
    budget = StringField("budget")
    email = StringField("Email", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    phone_number = StringField("Phone", validators=[InputRequired()])
    year = StringField("Year")
    plate = StringField("Plate")
    make = StringField()
    model = StringField()
    submit = SubmitField("Send Message")
