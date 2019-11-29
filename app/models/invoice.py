from datetime import datetime

from .. import db
from collections import OrderedDict


# invoice
class Invoice(db.Model):
    __tablename__ = "invoices"
    STATUS = OrderedDict([('pending', 'Pending'), ('rejected', 'Rejected'), ('approved', 'Approved')])
    id = db.Column(db.Integer, primary_key=True)
    invoice_no = db.Column(db.String(64))
    date_issued = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_due = db.Column(db.DateTime)
    status = db.Column(db.Enum(*STATUS, name='status_types', native_enum=False), index=True, nullable=True,
                       server_default='pending')
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'))
    payments = db.relationship('Payment', backref='invoice', lazy='dynamic', cascade='all,delete-orphan')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Invoice {}>'.format(self.id)
