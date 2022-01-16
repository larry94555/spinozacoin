from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
import logging
import os
from cryptography.hazmat.primitives import serialization
import yaml

def read_yaml(yamlFile):
    with open(yamlFile, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print(exc)
            return None

def config_logging(logFile, logLevel):
    format = "%(asctime)s: $(message)s"
    logging.basicConfig(format = format, filename = logFile, level = logLevel)

def create_directory_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_string_to_file(string, fileWithPath):
    with open(f"{fileWithPath}", "w") as textFile:
        textFile.write(str(string))
    
def generate_private_and_public_keys():
    curve = ec.SECP256K1()
    signatureAlgorithm = ec.ECDSA(hashes.SHA256())
    privateKey = ec.generate_private_key(curve)
    publicKeyValue = privateKey.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint).hex()
    privateKeyValue = privateKey.private_numbers().private_value
    return (privateKeyValue, publicKeyValue) 
    
def optional_s(count):
    return "s" if count > 1 else ""
