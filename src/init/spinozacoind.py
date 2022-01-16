# Copyright (c) 2021 SpinozaCoin developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/license/mit-license.php

import asyncio
import logging
from Node import Node
import util

async def main():
    config = util.read_yaml("../../config/spinozacoin.yml")
    if config == None:
       return
 
    util.config_logging("../../log/spinozacoind.log", config['loggingLevel'])

    # load up each instance which will have its secrets and will either be status "good" or status "bad"
    countInstances = config['countInstances']
    # add support for paths such as ~/spinozacoin
    loop = asyncio.get_event_loop()
    for instanceId in range(countInstances):

        # initiate a node
        node = Node(instanceId, config, loop)
        server = await node.join_network()

    print(f"All {countInstances} node{util.optional_s(countInstances)} have started")
    async with server:
        await server.serve_forever() 
          
if __name__ == "__main__":
    asyncio.run(main())

