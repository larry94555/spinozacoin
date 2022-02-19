# bootstap 
# -nc, --nodecount: specify the number of nodes at bootstrap (default: 1)
# -ip, --instancepath: specify the instancepath for directory, private key, etc.
# -bp, --baseport: specify the base port to be used 
# -h, --host: specify the host to be used

import argparse
import asyncio
import logging
from node import Node
from node_directory import NodeDirectory

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-nc", "--nodecount", help="number of nodes to bootstrap", type=int, default=1)
    parser.add_argument("-ip", "--instancepath", help="InstancePath to use for node", type=str, default="../../heartbeat")
    parser.add_argument("-bp", "--baseport", help="specify the base port to use for bootstraps", type=int, default=8888)
    parser.add_argument("-ho", "--host", help="specify the host to use for bootstraps", type=str, default="127.0.0.1")

    return parser.parse_args()

def main():
    args = parse_arguments()
    node_list=[Node(instance_id=instance_id, 
                    instance_path=f"{args.instancepath}/instance{instance_id}",
                    host=args.host,
                    port=args.baseport+instance_id
                   ) for instance_id in range(args.nodecount)]
    for node in node_list:
        node.directory.populate_bootstraps(node_list)
        node.start_heartbeat()

if __name__ == "__main__":
    main()

