#!/usr/bin/python3
# encoding: utf-8

from flask import Blueprint
import logging

from api import errors, responses

errorHandler = Blueprint("errorHandler", __name__)
log = logging.getLogger("errorHandler")

# JsonContentCorrupt
@errorHandler.app_errorhandler(errors.Unauthorized)
def handle_unauthorized(e):
    log.warning(e)
    return responses.UNAUTHORIZED("Authorization missing or failed.")

errorHandler.register_error_handler(401, handle_unauthorized)
