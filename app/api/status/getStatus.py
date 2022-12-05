#!/usr/bin/python3
# encoding: utf-8

from flask import Blueprint, Response
import json

getStatus = Blueprint("getStatus", __name__)

@getStatus.route('/reservations/status/', methods = ['GET'])
def get_status():
    status:json = {"apiversion": "1.3.0", "authors": ["Jakob Vollmer", "Louis Müller"]}
    return Response(json.dumps(status),  mimetype="application/json"), 200
