# -*- coding: utf-8 -*-
# Chon<chon219@gmail.com>

import os
import sys

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
admin = Admin(app)

from app.views import mod as mainModule
app.register_blueprint(mainModule)

from app.models import Account, Log
from flask.ext.admin.contrib.sqla import ModelView
admin.add_view(ModelView(Account, db.session))
admin.add_view(ModelView(Log, db.session))
