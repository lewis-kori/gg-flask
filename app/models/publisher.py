from .. import db
from datetime import datetime
from flask import current_app
from app.models.roles import Role

class Publisher(db.Model):
    __tablename__ = 'publishers'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120))
    overview = db.Column(db.String(2000))
    paypal   = db.Column(db.String(120))
    logo   = db.Column(db.String(120))
    banner   = db.Column(db.String(120))
    facebook   = db.Column(db.String(120))
    twitter   = db.Column(db.String(120))
    instagram   = db.Column(db.String(120))
    rating = db.Column(db.Integer(),default=0)
    overal_ratings = db.Column(db.Integer(),default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    phones = db.relationship('Pubphones', backref='profile',lazy='dynamic', cascade='all,delete-orphan')
    emails = db.relationship('Pubemails', backref='profile',lazy='dynamic', cascade='all,delete-orphan')
    locations = db.relationship('Publocations', backref='profile',lazy='dynamic', cascade='all,delete-orphan')

    def getLocations(self):
        data = self.locations.group_by(Publocations.make)
        return data


class Pubphones(db.Model):
    __tablename__ = 'pubphones'
    id = db.Column(db.Integer, primary_key=True)
    phone_number   = db.Column(db.String(120))
    publisher_id = db.Column(db.Integer(), db.ForeignKey('publishers.id'))

class Pubemails(db.Model):
    __tablename__ = 'pubemails'
    id = db.Column(db.Integer, primary_key=True)
    email   = db.Column(db.String(120))
    publisher_id = db.Column(db.Integer(), db.ForeignKey('publishers.id'))

class Publocations(db.Model):
    __tablename__ = 'Publocations'
    id = db.Column(db.Integer, primary_key=True)
    city   = db.Column(db.String(120))
    make   = db.Column(db.String(120))
    publisher_id = db.Column(db.Integer(), db.ForeignKey('publishers.id'))

    def get_count(self):
        return Publocations.query.filter_by(publisher_id=self.publisher_id).group_by(Publocations.publisher_id).count()
