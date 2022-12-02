#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
import os, requests

from api import errors
from const import DEFAULTS

def roomExists (roomId:str) -> None:
    assetsHost:str = os.getenv("BACKEND_ASSETS_HOST", DEFAULTS.BACKEND_ASSETS_HOST)
    jaegerTracecontextheadername:str = os.getenv("JAEGER_TRACECONTEXTHEADERNAME",  DEFAULTS.JAEGER_TRACECONTEXTHEADERNAME)

    headers:dict = {}
    if jaegerTracecontextheadername in request.headers:
        headers[jaegerTracecontextheadername] = request.headers[jaegerTracecontextheadername]

    response:requests.models.Response = requests.get(f"http://{assetsHost}/api/assets/rooms/{roomId}/", headers=headers)
    if (response.status_code != 200):
        raise errors.RoomNotFound(f"Room {roomId} not found. Status code of request {response.status_code}")
