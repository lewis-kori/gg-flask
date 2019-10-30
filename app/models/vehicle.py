from datetime import datetime

from .. import db

features_association = db.Table('features_association',
                                db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                                db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicles.id')),
                                db.Column('feature_id', db.Integer, db.ForeignKey('features.id'))
                                )


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    price = db.Column(db.String(80), index=True)
    description = db.Column(db.String(500), index=True)
    plate = db.Column(db.String(80), index=True)
    year = db.Column(db.String(80), index=True)
    featured = db.Column(db.Boolean, default=True, index=True)
    image_url = db.Column(db.String(64), index=True)
    front_image_url = db.Column(db.String(64), index=True)
    back_image_url = db.Column(db.String(64), index=True)
    right_image_url = db.Column(db.String(64), index=True)
    left_image_url = db.Column(db.String(64), index=True)
    dash_image_url = db.Column(db.String(64), index=True)
    interior_image_url = db.Column(db.String(64), index=True)
    extra_images_url = db.Column(db.String(500))
    mileage = db.Column(db.String(80), index=True)
    condition = db.Column(db.String(80), index=True)
    color = db.Column(db.String(80), index=True)
    model_id = db.Column(db.Integer(), db.ForeignKey('models.id'), index=True)
    make_id = db.Column(db.Integer(), db.ForeignKey('makes.id'), index=True)
    seller_name = db.Column(db.String(80), index=True)
    seller_email = db.Column(db.String(80), index=True)
    phone_number = db.Column(db.String(80), index=True)
    area = db.Column(db.String(80), index=True)
    fuel_type_id = db.Column(db.Integer(), db.ForeignKey('fuel_types.id'), index=True)
    transmission_id = db.Column(db.Integer, db.ForeignKey('transmissions.id'))
    engine_size = db.Column(db.String(80), index=True)
    interior = db.Column(db.String(80), index=True)
    features = db.relationship('Feature', secondary=features_association, backref='vehicle')
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Vehicle \'%s\'>' % self.name
