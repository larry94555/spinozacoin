# Copyright (c) 2021 SpinozaCoin developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/license/mit-license.php

import asyncio
from client import Client
from concurrent.futures.thread import ThreadPoolExecutor
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
import logging
import os
import time
import yaml

def create_directory_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_string_to_file(string, file_with_path):
    with open(f"{file_with_path}", "w") as text_file:
        text_file.write(str(string))

def create_secrets(secrets_path):
    curve = ec.SECP256K1()
    signature_algorithm = ec.ECDSA(hashes.SHA256())

    # Make private and public keys from the private value + curve
    priv_key = ec.generate_private_key(curve)
    pub_key = priv_key.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint).hex()
    priv_key_value = priv_key.private_numbers().private_value
    create_directory_if_needed(secrets_path)
    write_string_to_file(priv_key_value, f"{secrets_path}/node.private.key")
    write_string_to_file(pub_key, f"{secrets_path}/node.public.key")

async def register_with_trusted_node(trustedNode, port, root_port, loop):
    message = f"test: {trustedNode}:{port}"
    host = trustedNode
    # Connect with trustedNode
    print(f"handle_register connecting_to: host: {host}, port: {port}")
    try:
        transport, protocol = await loop.create_connection(Client,host=host, port=root_port)
        print(f"client connection succeeded: {message}")
        transport.write(f"{message}\n".encode())
        print(f"message sent... waiting for reply")
    except Exception as e:
        print(f"Connection to {host}:{port} failed with error: {e}")
    

async def handle_connection(reader, writer):
    # wait for message -- need to constrain by size 
    data = await reader.readuntil(b"\n")
    print(f"Server received: {data}")
    await writer.write("starting...\n".encode())
    print("After starting...")
    await writer.drain()

    writer.close()
    await writer.wait_closed()

async def start_node(instanceId, isLive, instanceBasePath, trustedNode, basePort, loop):
    print(f"\nstarting node: {trustedNode}:{instanceId+basePort}")
    instanceSecretsPath = f"{instanceBasePath}/instance{instanceId}/secrets"
    if not os.path.exists(f"{instanceSecretsPath}/node.private.key") or not os.path.exists(f"{instanceSecretsPath}/node.public.key"):
        create_secrets(instanceSecretsPath)

    if trustedNode != "127.0.0.1" or instanceId != 0:
        await register_with_trusted_node(trustedNode, basePort+instanceId, basePort, loop)

    server = await asyncio.start_server(handle_connection, trustedNode, basePort+instanceId)

    print(f"Node started: {trustedNode}:{instanceId+basePort}")
    return server

async def main():
    # parse config yml
    with open("../../config/spinozacoin.yml", "r") as stream:
        try:
            config=yaml.safe_load(stream)
       
        except yaml.YAMLError as exc:
            print(exc)

    # set up logging
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format = format, filename='../../log/spinozacoind.log', encoding='utf-8', level=config['loggingLevel'])

    # load up each instance which will have its secrets and will either be status "good" or status "bad"
    countInstances = config['countInstances']
    countDeadInstances = config['countDeadInstances']
    # add support for paths such as ~/spinozacoin
    instanceBasePath = os.path.expanduser(config['instanceBasePath'])
    loop = asyncio.get_event_loop()
    for instanceId in range(countInstances):
        # initiate a node
        server=await start_node(instanceId, instanceId >= countDeadInstances, instanceBasePath, config['trustedNode'], config['port'], loop)

    async with server:
        await server.serve_forever() 
          

if __name__ == "__main__":
    asyncio.run(main())

