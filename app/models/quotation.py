from datetime import datetime

from .. import db
from collections import OrderedDict


# quotations
class Quotation(db.Model):
    __tablename__ = "quotations"
    STATUS = OrderedDict([('pending', 'Pending'), ('rejected', 'Rejected'), ('approved', 'Approved')])
    id = db.Column(db.Integer, primary_key=True)
    quotation_name = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    quotation_no = db.Column(db.String(140))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    status = db.Column(db.Enum(*STATUS, name='status_types', native_enum=False), index=True, nullable=True,
                       server_default='pending')
    quotation_date = db.Column(db.DateTime, index=True)
    invoice = db.relationship('Invoice', backref='quotation', uselist=False, cascade='all,delete-orphan')
    products = db.relationship('Product', backref='quotation', lazy='dynamic', cascade='all,delete-orphan')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Quotation {}>'.format(self.id)
