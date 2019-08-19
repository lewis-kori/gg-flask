from .. import db


class Transmission(db.Model):
    __tablename__ = 'transmissions'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))

    def __repr__(self):
        return '<Transmission \'%s\'>' % self.type
