from os import environ

import requests
from dotenv import load_dotenv
load_dotenv()

host = str(environ.get('api_host'))
url_timeout = 30
headers = {'Content-Type': "application/json"}


def get_list_of_items(path: str):
    response = requests.get(url=host + path, timeout=url_timeout, verify=False)
    return response


def get_list_of_filtering_items(path: str, payload: dict):
    response = requests.get(url=host + path, params=payload, timeout=url_timeout, verify=False)
    return response


def get_item(path: str):
    response = requests.get(url=host + path, timeout=url_timeout, verify=False)
    return response


def create_item(path: str, json: dict = None, data: str = None):
    response = requests.post(url=host + path, data=data, json=json, timeout=url_timeout, headers=headers, verify=False)
    return response


def update_item(path: str, json: dict = None, data: str = None):
    response = requests.put(url=host + path, data=data, json=json, timeout=url_timeout, headers=headers, verify=False)
    return response


def delete_item(path):
    response = requests.delete(url=host + path, timeout=url_timeout, verify=False)
    return response
