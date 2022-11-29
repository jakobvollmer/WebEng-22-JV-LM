#!/usr/bin/python3
# encoding: utf-8

from flask import Blueprint
from flask import request

from api import errors
import logging

getStatus = Blueprint("getStatus", __name__)
log = logging.getLogger("getStatus")

@getStatus.route('/reservations/status/', methods = ['GET'])
def index():
    print(request.form)
    d = {"apiversion": "1.3.0", "authors": ["Jakob Vollmer", "Balast Müller"]}
    return d
