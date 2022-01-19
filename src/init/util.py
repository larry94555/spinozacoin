from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
import hashlib
import json
import logging
import os
from tinyec import registry
import secrets
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

def generate_alias():
    return "alias"

def generate_private_and_public_keys():
    curve = ec.SECP256K1()
    signatureAlgorithm = ec.ECDSA(hashes.SHA256())
    privateKey = ec.generate_private_key(curve)
    publicKeyValue = privateKey.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint).hex()
    privateKeyValue = privateKey.private_numbers().private_value
    return (privateKeyValue, publicKeyValue) 

def load_public_key():
    return None

def read_string_from_file(fileWithPath):
    with open(f"{fileWithPath}", "r") as textFile:
        return textFile.read()

def encode_action(sequence_id, timestamp, action, action_details):
    action = { 
        "sequence_id": sequence_id,
        "timestamp": timestamp,
        "action": action,
        "action_details": action_details
    }
    return json.dumps(action).encode() 

def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

def encrypt_action(private_key_value, sequence_id, timestamp, action, action_details):
    #curve = ec.SECP256K1()
    #curve = registry.get_curve("secp256r1")
    #cipher_text_public_key = secrets.randbelow(curve.field.n)
    #shared_ecc_key = cipher_text_public_key * private_key_value
    #secret_key = ecc_point_to_256_bit_key(shared_ecc_key)
    encoded_action = encode_action(sequence_id, timestamp, action, action_details)
    #cipher_text, nonce, auth_tag = encrypt_AES_GCM(encoded_action, secret_key)
    #cipher_text_private_key = cipher_text_public_key * curve.g
    #return (cipher_text, nonce, auth_tag, cipher_text_private_key)
    return encoded_action

def decrypt_action(encrypted_message, public_key_value):
    #(cipher_text, none, auth_tag, cipher_text_private_key) = encrypted_message 
    #shared_ecc_key = public_key_value * cipher_text_private_key
    #secret_key = ecc_point_to_256_bit_key(shared_ecc_key)
    #plain_text = decrypt_AES_GCM(cipher_text, nonce, auth_tag, secret_key)
    #return plaintext
    pass

def sign_action(private_key_value, sequence_id, timestamp, action, action_details):
    #curve = ec.SECP256K1()
    encoded_action = encode_action(sequence_id, timestamp, action, action_details)
    return encoded_action
    
def write_string_to_file(string, fileWithPath):
    with open(f"{fileWithPath}", "w") as textFile:
        textFile.write(str(string))
    
def optional_s(count):
    return "s" if count > 1 else ""
