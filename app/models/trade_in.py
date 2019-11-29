from datetime import datetime

from .. import db


# sell
class Tradein(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    transmission = db.Column(db.String(64))
    mileage = db.Column(db.String(64))
    year = db.Column(db.Integer)
    vin = db.Column(db.String(64))
    image = db.Column(db.String(64))
    exterior_color = db.Column(db.String(64))
    interior_color = db.Column(db.String(64))
    exterior_condition = db.Column(db.String(64))
    interior_condition = db.Column(db.String(64))
    accident = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    comments = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Tradein {}>'.format(self.id)
