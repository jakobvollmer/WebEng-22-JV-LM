#!/usr/bin/python3
# encoding: utf-8

from flask import request, Response, Blueprint
from typing import Tuple
import json, logging, uuid

from db.postqresDB import get_PostqresDB
from api.auth import auth
from api import responses
from api.tools import checkJsonFormat
from api.rooms import rooms

reservations = Blueprint("reservation", __name__)
postqresDB = get_PostqresDB()
log = logging.getLogger("api")

@reservations.route("/reservations", methods = ["GET"], strict_slashes=False)
def get_reservations_all():
    # Gets filter arguments. If filter doesnt exist -> var=None
    roomId = request.args.get("room_id")
    before = request.args.get("before")
    after = request.args.get("after")

    result = postqresDB.get_all_reservations(roomId, before, after)
    return Response(json.dumps(result),  mimetype="application/json"), 200

@reservations.route("/reservations/<id>", methods = ["GET"], strict_slashes=False)
def get_reservation_by_id(id):
    # Check if reservation exists.
    reservationById = postqresDB.get_reservation_by_id(id)
    if (reservationById == {}):
        return responses.NOT_FOUND("Reservation not found.")
    return Response(json.dumps(reservationById),  mimetype="application/json"), 200

@reservations.route("/reservations/<id>", methods = ["DELETE"], strict_slashes=False)
@auth.validateAuth
def delete_reservation_by_id(id):
    # Check if reservation exists.
    reservationById = postqresDB.get_reservation_by_id(id)
    if (reservationById == {}):
        return responses.NOT_FOUND("Reservation not found.")
        
    # Delete the reservation.
    postqresDB.delete_reservation_by_id(id)
    return Response(), 204

# This method just forwards the put request to the put_reservation method
@reservations.route("/reservations/<id>", methods = ["PUT"], strict_slashes=False)
def add_reservation_by_id(id):
    return put_reservation(id)

# This method just forwards the put request to the put_reservation method
@reservations.route("/reservations/", methods = ["POST"], strict_slashes=False)
def post_reservation():
    data = request.get_json()

    # If there's an id given in the post request it forwards the request to the put_reservation method
    # This is specified in the apidocs: "If the post method is called with an id, the put method is called"
    if "id" in data:
        log.info("Calling put")
        return put_reservation(data["id"])

    # If there is no id given create a uuid4 id and call the put_reservation method with the created id
    id = str(uuid.uuid4())
    return put_reservation(id)

def put_reservation (id:str) -> Tuple[Response, int]:
    # Check if reservation exists. If yes than the authentication has to be validated.
    reservationById = postqresDB.get_reservation_by_id(id)
    if (reservationById != {}):
        log.info(f"Need authentication because user wants to update reservation: {id}")
        auth.authenticate()

    # Check if the json format of the request is valid.
    data = request.get_json() 
    if not checkJsonFormat.isValid(data, checkJsonFormat.RESERVATION):
        log.info("Could not add/change reservation because json format is invalid")
        return responses.MISMATCHING_JSON_OBJECT()

    # Check if id in body and url are the same
    if "id" in data:
        if data["id"] != id:
            return responses.MISMATCHING_JSON_OBJECT()
            
    # Check if the room exists.
    if not rooms.roomExists(data["room_id"]):
        log.info("Could not add/change reservation because room does not exist.")
        return responses.MISMATCHING_JSON_OBJECT()

    # Check if the room has no other reservation in time span.
    if not postqresDB.room_has_no_other_reservation(id, data["room_id"], data["to"], data["from"]):
        log.info("Could not add/change reservation, because room is already taken in time span.")
        return responses.MISMATCHING_JSON_OBJECT()

    # Add or update reservation. Depending on if a reservation with id exists.
    if (reservationById == {}):
        log.info(f"Add new reservation: {id}")
        postqresDB.add_reservation(id, data["from"], data["to"], data["room_id"])
    else:
        log.info(f"Update reservation: {id}")
        postqresDB.update_reservation(id, data["from"], data["to"], data["room_id"])

    return Response(), 204