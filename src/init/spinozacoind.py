# Copyright (c) 2021 SpinozaCoin developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/license/mit-license.php

import asyncio
import logging
import yaml

class ConnectionPool:
    def __init__(self):
        self.connection_pool = set()

    def add_new_user_to_pool(self, writer):
        self.connection_pool.add(writer)

    def send_welcome_message(self, writer):
        message = "Hello, World!"
        writer.write(f"{message}\n".encode())

    def broadcast_user_join(self, writer):
        self.broadcast(writer, f"{writer.nickname} just joined")


async def handle_connection(reader, writer):
    print("\n\nA client connected....\n\n")
    connection_pool.add_new_user_to_pool(writer)
    connection_pool.send_welcome_message(writer)
    connection_pool.broadcast_user_join(writer)

async def main():
    # parse config yml
    with open("../../config/spinozacoin.yml", "r") as stream:
        try:
            config=yaml.safe_load(stream)
       
        except yaml.YAMLError as exc:
            print(exc)

    # set up logging
    logging.basicConfig(filename='../../log/spinozacoind.log', encoding='utf-8', level=config['loggingLevel'])
    logging.info(str(config))

    # load blockchains or create if empty
    # 1. nodes blockchain
    # 2. accounts blockchain
    # 3. transactions blockchain

        
    print("Awaiting broadcast...")
    server = await asyncio.start_server(handle_connection, "127.0.0.1", config["port"])


    async with server:
        await server.serve_forever()

connection_pool = ConnectionPool()
asyncio.run(main())

