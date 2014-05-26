# -*- coding: utf-8 -*-
# Chon<chon219@gmail.com>

from app import db
from datetime import datetime

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    create_date = db.Column(db.DateTime)

    def __init__(self, uid, name, phone):
        self.uid = uid
        self.name = name
        self.phone = phone
        self.create_date = datetime.now()

    def __unicode__(self):
        return "%s" % self.name

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    description = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('Account', 
            backref=db.backref('logs', lazy='dynamic'))

    def __init__(self, account, lat, lon, description):
        self.account = account
        self.lat = lat
        self.lon = lon
        self.description = description
        self.date = datetime.now()
