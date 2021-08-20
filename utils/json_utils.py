"""
JSON utilities.

Currently consists of loading and updating json files
"""
import json


def load_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def update_json(file_path, file_data):
    with open(file_path, "w") as file:
        json.dump(file_data, file)
