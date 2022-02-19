from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
import json
import os
from cryptography.hazmat.primitives import serialization

def backup_file(file_with_path, backup_history_size):
    for i in reversed(range(backup_history_size)):
        new_backup_file=f"{file_with_path}.bk{i+1}"
        old_backup_file=f"{file_with_path}.bk{i}" if i > 0 else f"{file_with_path}"
        if os.path.exists(new_backup_file):
            os.remove(new_backup_file)
            os.rename(old_backup_file, new_backup_file)

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

def get_private_key_from_serialized_value(private_key_file):
    private_key_bytes = read_bytes_from_file(private_key_file)
    return serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend()
    )

def get_public_key_from_serialized_value(public_key_file):
    public_key_bytes = read_bytes_from_file(public_key_file) 
    public_key = serialization.load_pem_public_key(public_key_bytes)
    return public_key.public_bytes(serialization.Encoding.X962, 
                                   serialization.PublicFormat.CompressedPoint).hex()

def read_bytes_from_file(file_with_path):
    with open(f"{file_with_path}", "rb") as byte_file:
        return byte_file.read()
 
def read_num_from_file(file_with_path):
    with open(f"{file_with_path}", "r") as text_file:
        return int(text_file.read())

def write_bytes_to_file(bytes, file_with_path):
    with open(f"{file_with_path}", "wb") as byte_file:
        byte_file.write(bytes)

def write_dict_to_file(dictionary, file_with_path):
    with open(f"{file_with_path}", "w") as text_file:
        text_file.write(json.dumps(dictionary))
