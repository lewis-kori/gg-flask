from datetime import datetime

from .. import db
from collections import OrderedDict


# bills
class Bill(db.Model):
    __tablename__ = "bills"
    STATUS = OrderedDict([('pending', 'Pending'), ('rejected', 'Rejected'), ('approved', 'Approved')])
    id = db.Column(db.Integer, primary_key=True)
    bill_name = db.Column(db.String(64))
    bill_no = db.Column(db.String(64))
    amount = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    status = db.Column(db.Enum(*STATUS, name='status_types', native_enum=False), index=True, nullable=True,
                       server_default='pending')
    date_issued = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    date_due = db.Column(db.DateTime, index=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Bill {}>'.format(self.id)
