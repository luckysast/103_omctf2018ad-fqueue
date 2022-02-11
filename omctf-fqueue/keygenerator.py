from base64 import b64encode
from os import urandom


def generate_key():
    return b64encode(urandom(24)).decode('utf-8')
