# -*- coding: utf-8 -*-
# Chon<chon219@gmail.com>

from flask import Blueprint, request, abort
import json
import hashlib

from app import db
from app.models import Account, Log
from config import TOKEN

mod = Blueprint('main', __name__)

def success(result):
    return json.dumps(dict(success=True, result=result))

def failure(msg):
    return json.dumps(dict(success=False, msg=msg))

@mod.route("/register", methods=['POST'])
def register():
    uid = request.form.get("uid")
    if not uid:
        return failure("invalid uid")
    name = request.form.get("name")
    if not name:
        return failure("invalid name")
    phone = request.form.get("phone")
    if not phone:
        return failure("invalid phone")
    account = Account.query.filter_by(uid=uid).first()
    if not account:
        account = Account(uid, name, phone)
        db.session.add(account)
        db.session.commit()
    return success(dict(name=account.name, phone=account.phone, uid=account.uid))

@mod.route("/checkin", methods=['POST'])
def checkin():
    uid = request.form.get("uid")
    if not uid:
        return failure("invalid uid")
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    if not lat or not lon:
        return failure("invalid lat or lon")
    description = request.form.get("description")
    account = Account.query.filter_by(uid=uid).first()
    if not account:
        return failure("account does not exist")
    log = Log(account, lat, lon, description)
    db.session.add(log)
    db.session.commit()
    return success(dict(uid=uid, lat=lat, lon=lon))

@mod.route("/verify", methods=['GET'])
def verify():
    sig = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")
    token = TOKEN
    sigstr = "".join(sorted([token, timestamp, nonce]))
    sighash = hashlib.sha1(sigstr).hexdigest()
    if sighash == sig:
        return echostr
    else:
        abort(404)
