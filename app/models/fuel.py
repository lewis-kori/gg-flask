from .. import db


class Fuel(db.Model):
    __tablename__ = 'fuel_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    vehicles = db.relationship('Vehicle', backref='Fuel', lazy='dynamic')

    def __repr__(self):
        return '<Fuel \'%s\'>' % self.name
