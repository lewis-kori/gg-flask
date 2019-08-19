from .. import db


class Transmission(db.Model):
    __tablename__ = 'transmissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    vehicles = db.relationship('Vehicle', backref='Transmission', lazy='dynamic')

    def __repr__(self):
        return '<Transmission \'%s\'>' % self.name
