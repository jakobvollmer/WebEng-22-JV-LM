#!/usr/bin/python3
# encoding: utf-8

from flask import request, Response, Blueprint
import json

from db.postqresDB import get_PostqresDB

getReservationsAll = Blueprint("getReservationsAll", __name__)
postqresDB = get_PostqresDB()

@getReservationsAll.route("/reservations", methods = ["GET"], strict_slashes=False)
def get_reservations_all():
    roomId = request.args.get("room_id")
    before = request.args.get("before")
    after = request.args.get("after")

    result = postqresDB.get_all_reservations(roomId, before, after)
    return Response(json.dumps(result),  mimetype="application/json"), 200