from datetime import datetime

from .. import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    price = db.Column(db.String(80), index=True)
    description = db.Column(db.String(500), index=True)
    plate = db.Column(db.String(80), index=True)
    year = db.Column(db.String(80), index=True)
    image_url = db.Column(db.String(64), index=True)
    mileage = db.Column(db.String(80), index=True)
    color = db.Column(db.String(80), index=True)
    model_id = db.Column(db.Integer(), db.ForeignKey('models.id'), index=True)
    make_id = db.Column(db.Integer(), db.ForeignKey('makes.id'), index=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Vehicle \'%s\'>' % self.name
