#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
from functools import wraps
import json, jwt, os, requests

from const import DEFAULTS
from api import errors

def getPublicKeyFromKeycloak () -> str:
    keycloakHost:str = os.getenv("KEYCLOAK_HOST", DEFAULTS.KEYCLOAK_HOST)
    keycloakRealm:str = os.getenv("KEYCLOAK_REALM", DEFAULTS.KEYCLOAK_REALM)
    jaegerTracecontextheadername:str = os.getenv("JAEGER_TRACECONTEXTHEADERNAME",  DEFAULTS.JAEGER_TRACECONTEXTHEADERNAME)

    # Set jaeger header for tracking
    headers:dict = {}
    if jaegerTracecontextheadername in request.headers:
        headers[jaegerTracecontextheadername] = request.headers[jaegerTracecontextheadername]

    # Get public key from keycloak
    response:requests.models.Response = requests.get(f"http://{keycloakHost}/auth/realms/{keycloakRealm}", headers=headers)
    content:json = json.loads(response.content)
    publicKey:str = content["public_key"]
    return (f"-----BEGIN PUBLIC KEY-----\n{publicKey}\n-----END PUBLIC KEY-----")

def authenticate ():
    # Check if authorization header is set
    if not "Authorization" in request.headers:
        raise errors.Unauthorized("No Authorization header supplied.")
    token:str = request.headers["Authorization"]

    # Check if token is from the correct specs
    if not token.startswith("Bearer"):
        raise errors.Unauthorized("Authorization header not to specs.")

    # Check if token signiture is signed correct
    try:
        publicKey:str = getPublicKeyFromKeycloak()
        decToken:json = jwt.decode(token[7:], publicKey, algorithms=["RS256"], audience="account")
    except Exception as e:
        raise errors.Unauthorized(f"Invalid Token. Exception: {e}")

def validateAuth(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):
        authenticate()        
        return f(*args,  **kwargs)  
    return decorator