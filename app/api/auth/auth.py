#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
from functools import wraps
import json, jwt, os, logging, requests

def getPublicKeyFromKeycloak () -> str:
    response:requests.models.Response = requests.get("http://localhost/auth/realms/biletado")
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
        except:
            raise Exception()
        
        return f(*args,  **kwargs)  
    return decorator