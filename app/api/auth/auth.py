#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request

def validateAuth () -> None:
    pass

"""
<?php

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

    /**
     * @throws GuzzleException
     */
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
}


"""