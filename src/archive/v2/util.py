import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from typing import Final
from cryptography.hazmat.primitives import hashes
import hashlib
import json
import logging
import math
import os
import random
from tinyec import registry
import secrets
from cryptography.hazmat.primitives import serialization
from datetime import timedelta
from datetime import timezone
import urllib.request
import yaml


# TO DO
# 
# 1. Consider dropping timestamp and using datetime directly

CURVE : Final = ec.SECP256K1()
SIGNATURE_ALGORITHM : Final = ec.ECDSA(hashes.SHA256())

random.seed(a=None)

def backup_file(file_with_path, backup_history_size):
    for i in reversed(range(backup_history_size)):
        new_backup_file=f"{file_with_path}.bk{i+1}"
        old_backup_file=f"{file_with_path}.bk{i}" if i > 0 else f"{file_with_path}"
        if os.path.exists(new_backup_file):  
            # copy previous version
            os.remove(new_backup_file)
            os.rename(old_backup_file, new_backup_file)
       

def config_logging(logFile, logLevel):
    format = "%(asctime)s: $(message)s"
    logging.basicConfig(format = format, filename = logFile, level = logLevel)

def create_directory_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)

# generate SHA256(x)
def generate_hash(hashable_string):
    return hashlib.sha256(hashable_string.encode()).hexdigest()

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

def get_external_ipv4():
    return urllib.request.urlopen("https://api.ipify.org").read().decode("utf8")

def get_external_ipv6():
    return urllib.request.urlopen("https://ident.me").read().decode("utf88")

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
    print(f"\nutil file with path: {file_with_path}")
    if not os.path.exists(file_with_path):
        write_num_to_file(1, file_with_path)
        return 1
    else:
        num = read_num_from_file(file_with_path)
        num += 1
        write_num_to_file(num, file_with_path)
        return num

def is_earlier_than(timestamp1, timestamp2):
    return fromtimestamp(timestamp1) < fromtimestamp(timestamp2)

def load_public_key():
    return None

def optional_s(count):
    return "s" if count > 1 else ""

# Random integer between 0 and size-1
def random_position(size):
    return random.randrange(size)

# find an x where gcd(x,size)=1
def random_step(size):
    if size == 1:
        return 1
    x = random.randrange(size-1)+1
    f = math.gcd(x,size)
    return x/f

def read_bytes_from_file(file_with_path):
    with open(f"{file_with_path}", "rb") as byte_file:
        return byte_file.read()

def read_dict_from_file(file_with_path):
    with open(f"{file_with_path}", "r") as text_file:
         return json.loads(text_file.read())

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

def seconds_ago(seconds):
    dt=now(timezone.utc) - timedelta(seconds=seconds)
    return dt.timestamp()

def utc_timestamp():
    dt = datetime.datetime.now(timezone.utc)
    return dt.timestamp()

def validate_signature(public_key, signature, json_string):
    try:
        signature_algorithm = ec.ECDSA(hashes.SHA256())
        public_key.verify(signature, json_string, signature_algorithm)
    except InvalidSignature as e:
        print(f"Invalid: exception: {e}")
        return False
    return True

def write_bytes_to_file(bytes, file_with_path):
    with open(f"{file_with_path}", "wb") as byte_file:
        byte_file.write(bytes)

def write_dict_to_file(dictionary, file_with_path):
    with open(f"{file_with_path}", "w") as text_file:
        text_file.write(json.dumps(dictionary))

def write_num_to_file(num, file_with_path):
    with open(f"{file_with_path}", "w") as text_file:
        text_file.write(str(num))
    
