#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request
import json, jwt, os, logging, requests

def validateAuth () -> None:
    if not "Authorization" in request.headers:
        raise Exception("No Authorization header supplied.")
    token = request.headers["Authorization"]

    if not token.startswith("Bearer"):
        raise Exception("Authorization header not to specs.")

    #try:
    publicKey = getPublicKeyFromKeycloak()
    print(publicKey)
    #jwt.decode(token[7:], publicKey, algorithms=["RS256"])

        #JWT::decode(substr(string: $token, offset: 7), new Key(keyMaterial: $publicKey,  algorithm: 'RS256'));
    #except:
    #    raise Exception()

            
def getPublicKeyFromKeycloak () -> str:
    response = requests.get("http://localhost/auth/realms/biletado")
    content:json = json.loads(response.content)
    publicKey:str = content["public_key"]
    return (f"-----BEGIN PUBLIC KEY-----\n{publicKey}\n-----END PUBLIC KEY-----")

"""
<?php
    private function getPublicKeyFromKeycloak(): string {
        $client = new Client(config: [
            'base_uri' => 'http://' . env(key: 'KEYCLOAK_HOST'),
            'headers' => [
                env(key: 'JAEGER_TRACECONTEXTHEADERNAME', default: 'uber-trace-id') => session(key: 'jaeger-token')
            ]
        ]);
        $uri = new Uri(uri: "/auth/realms/" . env(key: 'KEYCLOAK_REALM'));

        $response = $client->request(
            method: 'GET',
            uri: $uri,
            options: [
                'verify'  => false,
            ]
        );

        $body = json_decode(json: $response->getBody()->getContents(), associative: true);
        return strtr(
            "-----BEGIN PUBLIC KEY-----\n:key\n-----END PUBLIC KEY-----",
            [':key' => $body['public_key']]
        );
    }

    private function validateAuth(Request $request): void
    {
        if (!$request->hasHeader(key: 'Authorization')) {
            throw new UnauthorizedException(message: "No Authorization header supplied.");
        }
        $token = $request->header(key: 'Authorization');
        if (!str_starts_with(haystack: $token, needle: 'Bearer ')) {
            throw new UnauthorizedException(message: "Authorization header not to specs.");
        }

        try {
            $publicKey = $this->getPublicKeyFromKeycloak();
            JWT::decode(substr(string: $token, offset: 7), new Key(keyMaterial: $publicKey,  algorithm: 'RS256'));
            //If token is invalid, this will fail
        } catch (Exception $exception) {
            throw new UnauthorizedException(message: $exception->getMessage());
        } catch (GuzzleException $exception) {
            throw new UnauthorizedException(message: $exception->getMessage());
        }
    }
}


"""