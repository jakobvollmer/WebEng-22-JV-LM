#!/usr/bin/python3
# encoding: utf-8

from flask import Blueprint

from api import errors
import logging

errorHandler = Blueprint("errorHandler", __name__)
log = logging.getLogger("errorHandler")

# JsonContentCorrupt
@errorHandler.app_errorhandler(errors.Unauthorized)
def handle_JsonContentCorrupt(e):
    log.warning(e)
    return "TEST"

errorHandler.register_error_handler(401, handle_JsonContentCorrupt)
