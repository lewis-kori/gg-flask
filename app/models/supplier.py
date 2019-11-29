from datetime import datetime

from .. import db


class Supplier(db.Model):
    __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(64))
    supplier_type = db.Column(db.String(64))
    phone_number = db.Column(db.Integer, index=True)
    email = db.Column(db.String(64), index=True)
    location = db.Column(db.String(140))
    bank_name = db.Column(db.String(64))
    bank_country = db.Column(db.String(64))
    bank_address = db.Column(db.String(120))
    account_number = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    bills = db.relationship('Bill', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return '<Client {}>'.format(self.id)
