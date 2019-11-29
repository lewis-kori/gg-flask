from datetime import datetime
from app import db


#clients
class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(64))
    client_type = db.Column(db.String(64))
    phone_number = db.Column(db.Integer, index=True)
    email = db.Column(db.String(64), index=True)
    location = db.Column(db.String(140))
    quotations = db.relationship('Quotation', backref='client', lazy='dynamic')
    enquiries = db.relationship('Enquiry', backref='client', lazy='dynamic')
    imports = db.relationship('Import', backref='client', lazy='dynamic')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Client {}>'.format(self.id)
