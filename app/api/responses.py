#!/usr/bin/python3
# encoding: utf-8

from flask import Response
from typing import Tuple
import json

def NOT_FOUND (message:str) -> Tuple[Response, int]:
    return Response(json.dumps({"message" : message, "additionalProp1": {}}),  mimetype="application/json"), 404

def UNAUTHORIZED (message:str) -> Tuple[Response, int]:
    return Response(json.dumps({"message" : message, "additionalProp1": {}}),  mimetype="application/json"), 401

def InternalServerError () -> Tuple[Response, int]:
    return Response(json.dumps({"message" : "The server encountered an internal error and was unable to complete your request.", "additionalProp1": {}}),  mimetype="application/json"), 500
