#!/bin/python3
import http.client
import json

conn = http.client.HTTPSConnection("pokeapi.co")

conn.request("GET", "/api/v2/pokemon/1/")

res = conn.getresponse()
data = res.read().decode("utf-8")

with open("pokedex.json", "w") as file:
    file.write(json.dumps(json.loads(data), indent=4, sort_keys=False))
