#!/usr/bin/python3
# encoding: utf-8

from flask import request, Response, Blueprint
import json, logging

from db.postqresDB import get_PostqresDB
from api.auth.auth import validateAuth
from api import errors, responses
from api.tools import checkJsonFormat
from api.rooms import rooms

reservations = Blueprint("reservation", __name__)
postqresDB = get_PostqresDB()
log = logging.getLogger("api")

@reservations.route("/reservations", methods = ["GET"], strict_slashes=False)
def get_reservations_all():
    roomId = request.args.get("room_id")
    before = request.args.get("before")
    after = request.args.get("after")

    result = postqresDB.get_all_reservations(roomId, before, after)
    return Response(json.dumps(result),  mimetype="application/json"), 200

@reservations.route("/reservations/<id>", methods = ["GET"], strict_slashes=False)
def get_reservation_by_id(id):
    result = postqresDB.get_reservation_by_id(id)
    if (result == {}):
        return responses.NOT_FOUND("Reservation not found.")
    return Response(json.dumps(result),  mimetype="application/json"), 200

@reservations.route("/reservations/<id>", methods = ["DELETE"], strict_slashes=False)
@validateAuth
def delete_reservation_by_id(id):
    result = postqresDB.get_reservation_by_id(id)
    if (result == {}):
        return responses.NOT_FOUND("Reservation not found.")
    postqresDB.delete_reservation_by_id(id)
    return Response(), 204

@reservations.route("/reservations/<id>", methods = ["PUT"], strict_slashes=False)
#@validateAuth
def add_reservation_by_id(id):
    data = request.get_json() 
    if not checkJsonFormat.isValid(data, checkJsonFormat.RESERVATION):
        log.info("Could not add/change reservation because json format is invalid")
        return responses.MismatchingJsonObject()

    if not rooms.roomExists(data["room_id"]):
        log.info("Could not add/change reservation because room does not exist.")
        return responses.MismatchingJsonObject()

    if not postqresDB.room_has_no_other_reservation(id, data["room_id"], data["to"], data["from"]):
        log.info("Could not add/change reservation, because room is already taken in time span.")
        return responses.MismatchingJsonObject()

    result = postqresDB.get_reservation_by_id(id)
    if (result == {}):
        log.info(f"Add new reservation: {id}")
        postqresDB.add_reservation(id, data["from"], data["to"], data["room_id"])
    else:
        log.info(f"Update new reservation: {id}")
        postqresDB.update_reservation(id, data["from"], data["to"], data["room_id"])

    return Response(), 204