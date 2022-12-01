#!/usr/bin/python3
# encoding: utf-8

from flask import request, Response, Blueprint
import json

from db.postqresDB import get_PostqresDB
from api.auth.auth import validateAuth
from api import errors, responses

reservations = Blueprint("reservation", __name__)
postqresDB = get_PostqresDB()

@reservations.route("/reservations", methods = ["GET"], strict_slashes=False)
def get_reservations_all():
    roomId = request.args.get("room_id")
    before = request.args.get("before")
    after = request.args.get("after")

    result = postqresDB.get_all_reservations(roomId, before, after)
    return Response(json.dumps(result),  mimetype="application/json"), 200

@reservations.route("/reservations/<id>", methods = ["GET"], strict_slashes=False)
def get_reservations_by_id(id):
    result = postqresDB.get_reservation_by_id(id)
    if (result == {}):
        return responses.NOT_FOUND("Reservation not found.")
    return Response(json.dumps(result),  mimetype="application/json"), 200

@reservations.route("/reservations/<id>", methods = ["DELETE"], strict_slashes=False)
@validateAuth
def delete_reservations_by_id(id):
    result = postqresDB.get_reservation_by_id(id)
    if (result == {}):
        return responses.NOT_FOUND("Reservation not found.")
    postqresDB.delete_reservation_by_id(id)
    return Response(), 204