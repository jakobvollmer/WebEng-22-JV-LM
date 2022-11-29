#!/usr/bin/python3
# encoding: utf-8

from flask import Blueprint
from flask import request

from api import errors
import logging

getAll = Blueprint("getAll", __name__)
log = logging.getLogger("getAll")

@getAll.route('/reservations/', methods = ['GET'])
def index():
    print(request.form)
    return 'Web App with Python Flask! TEST'