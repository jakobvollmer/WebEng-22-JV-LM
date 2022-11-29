#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
from functools import wraps
import json, jwt, os, requests

def getPublicKeyFromKeycloak () -> str:
    keycloakHost:str = os.getenv("KEYCLOAK_HOST", "localhost")
    keycloakRealm:str = os.getenv("KEYCLOAK_REALM", "biletado")

    jaegerTracecontextheadername:str = os.getenv("JAEGER_TRACECONTEXTHEADERNAME", "uber-trace-id")

    headers = {}
    if jaegerTracecontextheadername in request.headers:
        headers[jaegerTracecontextheadername] = request.headers[jaegerTracecontextheadername]

    response:requests.models.Response = requests.get(f"http://{keycloakHost}/auth/realms/{keycloakRealm}", headers=headers)
    content:json = json.loads(response.content)
    publicKey:str = content["public_key"]
    return (f"-----BEGIN PUBLIC KEY-----\n{publicKey}\n-----END PUBLIC KEY-----")

def validateAuth(f):  
    @wraps(f)  
    def decorator(*args, **kwargs):
        if not "Authorization" in request.headers:
            raise Exception("No Authorization header supplied.")
        token = request.headers["Authorization"]

        if not token.startswith("Bearer"):
            raise Exception("Authorization header not to specs.")

        try:
            publicKey = getPublicKeyFromKeycloak()
            decToken:json = jwt.decode(token[7:], publicKey, algorithms=["RS256"], audience="account")
        except Exception as e:
            raise Exception(e)
        
        return f(*args,  **kwargs)  
    return decorator