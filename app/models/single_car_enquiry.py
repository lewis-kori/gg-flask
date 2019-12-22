from datetime import datetime

from .. import db


class SingleEnquiry(db.Model):
    __tablename__ = "single_car_enquiries"
    id = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.String(80))
    message = db.Column(db.String(200))
    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    phone_number = db.Column(db.String(80))
    plate = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    year = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<SingleEnquiry {}>'.format(self.id)


