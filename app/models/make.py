from datetime import datetime
from .. import db


class Make(db.Model):
    __tablename__ = 'makes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    image_url = db.Column(db.String(64), index=True)
    description = db.Column(db.String(10000))
    models = db.relationship('Model', backref='make', lazy='dynamic')
    vehicles = db.relationship('Vehicle', backref='make', lazy='dynamic')
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Make \'%s\'>' % self.name

