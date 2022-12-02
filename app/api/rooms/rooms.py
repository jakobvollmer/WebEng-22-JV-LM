#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
import os, requests

from api import errors
from const import DEFAULTS

def roomExists (roomId:str) -> bool:
    assetsHost:str = os.getenv("BACKEND_ASSETS_HOST", DEFAULTS.BACKEND_ASSETS_HOST)
    jaegerTracecontextheadername:str = os.getenv("JAEGER_TRACECONTEXTHEADERNAME",  DEFAULTS.JAEGER_TRACECONTEXTHEADERNAME)

    # Set jaeger header for tracking
    headers:dict = {}
    if jaegerTracecontextheadername in request.headers:
        headers[jaegerTracecontextheadername] = request.headers[jaegerTracecontextheadername]

    # Get room from assets-backend
    response:requests.models.Response = requests.get(f"http://{assetsHost}/api/assets/rooms/{roomId}/", headers=headers)
    if (response.status_code != 200):
        return False
    return True
