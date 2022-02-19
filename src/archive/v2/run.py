import argparse
import asyncio
from config import Config
from server import Server
import util

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments for log file and configuration file
    parser.add_argument("-i", "--ip", help="InstancePath to use for node", type=str, default="../..")
    return parser.parse_args()

def main():
    args = parse_arguments()

    config = Config(args.ip)
    util.config_logging(f"{args.ip}/log/spinozacoin.log", config.get_logging_level())

    loop = asyncio.get_event_loop()
    for instance_id in range(config.get_count_instances()):
        
        # initiate nodes to simulate a simple network
        print(f"\nStarting instance {instance_id}\n")
        server = Server(instance_id, config, loop) 
        server.run()

    #async with server:
    #    await server.serve_forever()


if __name__ == "__main__":
    #asyncio.run(main())
    main()
