"""
Helper class for managing receipts
"""
import util

class NodeReceipts:
    """
    Main class for node receipts.
    """
    def __init__(self):
        self.receipts_for_node = {}
        self.receipts_for_current_neighborhood = {}
        self.receipts_for_next_neighborhood = {}
        self.__public_key = None
        self.__private_key = None

    def get_private_key(self):
        """
        return private key
        """
        return self.__private_key

    def get_public_key(self):
        """
        return public key
        """
        return self.__public_key

    def set_private_key(self, private_key):
        """
        set private key
        """
        self.__private_key = private_key

    def set_public_key(self, public_key):
        """
        set public key
        """
        self.__public_key = public_key

    def create_secrets(self, private_key_file, public_key_file):
        """
        create secrets
        """
        self.__private_key, self.__public_key = util.generate_private_and_public_keys()
        util.write_bytes_to_file(self.__private_key, private_key_file)
        util.write_bytes_to_file(self.__public_key, public_key_file)
