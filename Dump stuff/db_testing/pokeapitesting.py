import time
import requests
import json
from utils.json_utils import load_json, create_json, update_json

id = 493

def call(print_resp=False, id=id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{id}/"
    response = requests.request("GET", url=url)
    data = json.loads(response.text)
    if print_resp:
        print(json.dumps(data, indent=4, sort_keys=False))
    else:
        update_json("dump.json", data, operation="w")

def list(print_resp=False):
    begin, end = 1,5
    for i in range(begin, end+1):
        call(print_resp, id=i)
        time.sleep(1)


call()