from datetime import datetime

from .. import db
from collections import OrderedDict


# payment
class Payment(db.Model):
    __tablename__ = "payments"
    STATUS = OrderedDict([('pending', 'Pending'), ('rejected', 'Rejected'), ('approved', 'Approved')])
    MODE = OrderedDict([('cash', 'Cash'), ('cheque', 'Cheque'), ('online-payment', 'Online-Payment')])
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(2000))
    amount = db.Column(db.Integer)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))
    status = db.Column(db.Enum(*STATUS, name='status_types', native_enum=False), index=True, nullable=True,
                       server_default='pending')
    payment_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    payment_mode = db.Column(db.Enum(*MODE, name='payment_mode', native_enum=False), index=True, nullable=True,
                             server_default='cash')
    payment_type = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Payment {}>'.format(self.id)
