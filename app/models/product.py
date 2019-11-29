from datetime import datetime

from .. import db
from collections import OrderedDict


# product
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(64))
    size = db.Column(db.String(64))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    total = db.Column(db.Integer)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'))

    def __repr__(self):
        return '<Product {}>'.format(self.id)
