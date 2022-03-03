"""
bootstap
 -nc, --nodecount: specify the number of nodes at bootstrap (default: 1)
 -ip, --instancepath: specify the instancepath for directory, private key, etc.
 -bp, --baseport: specify the base port to be used
 -h, --host: specify the host to be used
"""

import argparse
import asyncio
import logging

from node import Node
from node import Status
from node_info import NodeInfo

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

def parse_arguments():
    """
    Parse optional arguments: -nc, -ip, -bp, -ho
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-nc", "--nodecount", help="number of nodes to bootstrap", type=int,
                        default=1)
    parser.add_argument("-ip", "--instancepath", help="InstancePath to use for node", type=str,
                        default="../../test")
    parser.add_argument("-bp", "--baseport", help="specify the base port to use for bootstraps",
                        type=int, default=6100)
    parser.add_argument("-ho", "--host", help="specify the host to use for bootstraps", type=str,
                        default="127.0.0.1")

    return parser.parse_args()

def main():
    """
    bootstrap -nc nodes which can be used for demos and testing
    """
    args = parse_arguments()
    node_list=[Node(NodeInfo(instance_id,
                              args.host,
                              args.baseport+instance_id,
                              f"{args.instancepath}/instance{instance_id}"),
                    node_id=instance_id+1,
                    status=Status.UP) for instance_id in range(args.nodecount)]

    print(f"main: list: {len(node_list)}")

    for i, node in enumerate(node_list):
        print(f"\ni: {i}, port: {node.info.port}")
        node.directory.populate_bootstraps(node_list, node.get_neighborhood_size())
        try:
            node.listen()
        except OSError as oe:
            print(f"\nCaught error: {oe}")
            exit()
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    main()
