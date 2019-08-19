from flask_wtf import Form, FlaskForm
from wtforms import ValidationError
from flask_ckeditor import CKEditorField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    TextAreaField,
    FileField,
    FormField,
    HiddenField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import db
from app.models import Role, User, Category

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
    description = TextAreaField("Description", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
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
    front_image = StringField(
        validators=[InputRequired()]
    )
    back_image = HiddenField(
    )
    left_image = HiddenField(
    )
    right_image = HiddenField(
    )
    dash_image = HiddenField(
    )
    interior_image = HiddenField(
    )
    seller_email = StringField('Email', validators=[InputRequired()])
    seller_name = StringField('Name', validators=[InputRequired()])
    phone_number = StringField('Phone', validators=[InputRequired()])
    area = StringField('Area', validators=[InputRequired()])
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
    name = StringField("Name", validators=[InputRequired(), Length(1, 64)])
    description = TextAreaField(
        "Description", validators=[InputRequired(), Length(1, 64)]
    )
    price = StringField("Price", validators=[InputRequired()])
    mileage = StringField("Mileage", validators=[InputRequired()])
    color = StringField("Color", validators=[InputRequired()])
    plate = StringField("Plate", validators=[InputRequired()])
    year = StringField("Year", validators=[InputRequired()])
    image_url = FileField(validators=[FileAllowed(photos, u"Image only!")])
    model_id = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    make_id = SelectField(validators=[InputRequired()], choices=[], coerce=int)
    submit = SubmitField("Add")


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
