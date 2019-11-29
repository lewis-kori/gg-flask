from datetime import datetime
from app import db
from flask import current_app, url_for


# Bazaar
class Bazaar(db.Model):
    __tablename__ = "bazaars"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    location = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    color = db.Column(db.String(120))
    vehicles = db.relationship('Vehicle', backref='bazaar', lazy='dynamic')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Bazaar {}>'.format(self.id)
