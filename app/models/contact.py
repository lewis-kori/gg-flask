from datetime import datetime
from app import db


class Contact(db.Model):
    __tablename__ = "contact_us"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    message = db.Column(db.String(120))
    subject = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Contact {}>'.format(self.id)
