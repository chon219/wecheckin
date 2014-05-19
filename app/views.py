# -*- coding: utf-8 -*-
# Chon<chon219@gmail.com>

from flask import Blueprint, request, abort
import json
import hashlib

from app import db
from app.models import Account, Log
from config import TOKEN

mod = Blueprint('main', __name__)

@mod.route("/register", methods=['POST'])
def register():
    uid = request.form.get("uid")
    name = request.form.get("name")
    phone = request.form.get("phone")
    account = Account(uid, name, phone)
    db.session.add(account)
    db.session.commit()
    return json.dumps(dict(name=name, phone=phone, uid=uid))

@mod.route("/checkin", methods=['POST'])
def checkin():
    uid = int(request.form.get("uid"))
    lat = int(request.form.get("lat"))
    lon = int(request.form.get("lon"))
    account = Account.query.filter_by(uid=uid).first_or_404()
    log = Log(account, lat, lon)
    db.session.add(log)
    db.session.commit()
    return json.dumps(dict(uid=uid, lat=lat, lon=lon))

@mod.route("/verify", methods=['GET'])
def verify():
    sig = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")
    token = TOKEN
    sigstr = "".join(sorted([token, timestamp, nonce]))
    sighash = hashlib.sha1(sigstr).hexdigest()
    if sigtmp == sig:
        return echostr
    else:
        abort(404)
