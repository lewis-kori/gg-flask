from datetime import datetime

from .. import db


class SellersVehicle(db.Model):
    __tablename__ = 'sellers_vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    price = db.Column(db.String(80), index=True)
    description = db.Column(db.String(500), index=True)
    plate = db.Column(db.String(80), index=True)
    year = db.Column(db.String(80), index=True)
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
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<SellersVehicle \'%s\'>' % self.name
