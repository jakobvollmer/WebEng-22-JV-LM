#!/usr/bin/python3
# encoding: utf-8

from flask import Blueprint, request
import logging

from api import errors, responses

errorHandler = Blueprint("errorHandler", __name__)
log = logging.getLogger("errorHandler")

# Unauthorized
@errorHandler.app_errorhandler(errors.Unauthorized)
def handle_unauthorized(e):
    log.warning("Exception Unauthorized raised at request " + request.base_url + " . Exception: " + str(e))
    return responses.UNAUTHORIZED("Authorization missing or failed.")

# InternalServerError
@errorHandler.app_errorhandler(errors.InternalServerError)
def handle_internal_server_error(e):
    log.warning("Exception InternalServerError raised. Exception: " + str(e))
    return responses.InternalServerError()

errorHandler.register_error_handler(401, handle_unauthorized)
errorHandler.register_error_handler(500, handle_internal_server_error)
