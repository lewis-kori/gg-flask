from datetime import datetime

from .. import db
from ..models import Vehicle, Client
from collections import OrderedDict


# enquiries
class Enquiry(db.Model):
    __tablename__ = "enquiries"
    id = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Numeric)
    year = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    # created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Enquiry {}>'.format(self.id)

    def from_enquiry_dict(self, data):
        for field in ['model', 'budget', 'client', 'year']:
            if field in data:
                if field == 'model':
                    id = data[field]
                    field = 'vehicle'
                    vehicle = Vehicle.query.get_or_404(id)
                    setattr(self, field, vehicle)
                elif field == 'client':
                    print('here')
                    id = data[field]
                    field = 'client'
                    client = Client.query.get_or_404(id)
                    setattr(self, field, client)
                else:
                    setattr(self, field, data[field])
