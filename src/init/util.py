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

def create_directory_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_private_and_public_keys():
    curve = ec.SECP256K1()
    private_key = ec.generate_private_key(curve)
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

def increase_and_return_value(path, filename):
    file_with_path=f"{path}/{filename}"
    print(f"file with path: {file_with_path}")
    if not os.path.exists(file_with_path):
        write_num_to_file(1, file_with_path)
        return 1
    else:
        num = read_num_from_file(file_with_path)
        num += 1
        write_num_to_file(num, file_with_path)
        return num


def load_public_key():
    return None

def optional_s(count):
    return "s" if count > 1 else ""

def read_bytes_from_file(file_with_path):
    with open(f"{file_with_path}", "rb") as byte_file:
        return byte_file.read()

def read_num_from_file(file_with_path):
    with open(f"{file_with_path}", "r") as text_file:
         return int(text_file.read())

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

def write_bytes_to_file(bytes, file_with_path):
    with open(f"{file_with_path}", "wb") as byte_file:
        byte_file.write(bytes)

def write_num_to_file(num, file_with_path):
    with open(f"{file_with_path}", "w") as text_file:
        text_file.write(str(num))
    
