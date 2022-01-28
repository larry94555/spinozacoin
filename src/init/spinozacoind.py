# Copyright (c) 2021 SpinozaCoin developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/license/mit-license.php

# The application should provide a server rich enough that it is straight forward to write a simple api to do one of the following:
# 1.  Get status of server ("up", "joining", "down", "flagged")
# 2.  Add a new node
# 3.  Add a wallet
# 4.  Add an application that runs on top of the network (ie a smart contract)

import asyncio
from config import Config
from typing import Final
import logging
from node import Node
import util

SPINOZA_COIN_YAML_FILE : Final = "../../config/spinozacoin.yml"
SPINOZA_COIN_LOG_FILE : Final = "../../log/spinozacoind.log"

async def main():

    config = Config(SPINOZA_COIN_YAML_FILE)
    util.config_logging(SPINOZA_COIN_LOG_FILE, config.get_logging_level())

    # load up each instance which will have its secrets and will either be status "good" or status "bad"
    count_instances = config.get_count_instances()
    # add support for paths such as ~/spinozacoin
    loop = asyncio.get_event_loop()
    for instance_id in range(count_instances):

        # initiate a node
        node = Node(instance_id, config, loop)
        server = await node.join_network()

    print(f"{count_instances} node{util.optional_s(count_instances)} have started")
    async with server:
        await server.serve_forever() 
          
if __name__ == "__main__":
    asyncio.run(main())

