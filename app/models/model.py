from datetime import datetime

from .. import db


class Model(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(10000))
    image_url = db.Column(db.String(64), index=True)
    make_id = db.Column(db.Integer(), db.ForeignKey('makes.id'), index=True)
    vehicles = db.relationship('Vehicle', backref='model', lazy='dynamic')
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Model \'%s\'>' % self.name
