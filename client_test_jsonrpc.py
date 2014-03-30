#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc

http_client = pyjsonrpc.HttpClient(
    url = "http://localhost:8080",
    username = "Username",
    password = "Password"
)
print http_client.call("add", 1, 2)
# Result: 3

# It is also possible to use the *method* name as *attribute* name.
print http_client.add(1, 2)
# Result: 3