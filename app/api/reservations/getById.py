#!/usr/bin/python3
# encoding: utf-8

from flask import request, Response, Blueprint
import json

from api import errors
from db.postqresDB import get_PostqresDB

getReservationsById = Blueprint("getReservationsById", __name__)
postqresDB = get_PostqresDB()

@getReservationsById.route("/reservations/<id>", methods = ["GET"], strict_slashes=False)
def get_reservations_by_id(id):
    result = postqresDB.get_reservation_by_id(id)
    if (result == {}):
        return 
    return Response(json.dumps(result),  mimetype="application/json"), 200