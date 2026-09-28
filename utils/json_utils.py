# utils/json_utils.py
import json


def json_to_dict(structured_str : str):
    return json.loads(structured_str)
