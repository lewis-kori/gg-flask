from .. import db


class Fuel(db.Model):
    __tablename__ = 'fuel_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))

    def __repr__(self):
        return '<Fuel \'%s\'>' % self.type
