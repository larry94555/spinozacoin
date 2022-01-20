import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from typing import Final
from cryptography.hazmat.primitives import hashes
import hashlib
import json
import logging
import os
from tinyec import registry
import secrets
from cryptography.hazmat.primitives import serialization
from datetime import timezone
import yaml

CURVE : Final = ec.SECP256K1()
SIGNATURE_ALGORITHM : Final = ec.ECDSA(hashes.SHA256())


def config_logging(logFile, logLevel):
    format = "%(asctime)s: $(message)s"
    logging.basicConfig(format = format, filename = logFile, level = logLevel)

def convert_dict_to_json_string(dictionary, indent=4):
    return json.dumps(dictionary, indent=indent)

def create_directory_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_alias():
    return "alias"

def generate_private_and_public_keys():
    curve = ec.SECP256K1()
    #signature_algorithm = ec.ECDSA(hashes.SHA256())
    private_key = ec.generate_private_key(curve)
    #publicKeyValue = privateKey.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint).hex()
    #privateKeyValue = privateKey.private_numbers().private_value
    #return (privateKeyValue, publicKeyValue) 
    serialized_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption() 
    )
    public_key = private_key.public_key()
    serialized_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return (serialized_private_key, serialized_public_key)

def get_public_key_value_from_serialized_value(serialized_public_key):
    public_key = serialization.load_pem_public_key(serialized_public_key)
    return public_key.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.CompressedPoint).hex()

def get_private_key_from_serialized_value(serialized_private_key):
    return serialization.load_pem_private_key(
        serialized_private_key,
        password=None,
        backend=default_backend()
    )

def get_signature_for_json(private_key, json_string):
    return private_key.sign(json_string.encode(), SIGNATURE_ALGORITHM)

def load_public_key():
    return None

def optional_s(count):
    return "s" if count > 1 else ""

def read_bytes_from_file(fileWithPath):
    with open(f"{fileWithPath}", "rb") as byte_file:
        return byte_file.read()

def read_yaml(yamlFile):
    with open(yamlFile, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print(exc)
            return None

def utc_timestamp():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    return utc_time.timestamp()
   

def write_bytes_to_file(bytes, fileWithPath):
    with open(f"{fileWithPath}", "wb") as byte_file:
        byte_file.write(bytes)
    
