class Protocol:

    def __init__(self):
        self.prefix = "007"
        pass 

    def announce(self, host, port, privateKey, publicKey, writer, reader):
        # pass public key, (ip, port, timestamp, order).signed, nonce (simple pow)
        # either qualified or rejected.
        signed=util.signWithKey(privateKey, ip, port, order)
        payload=util.generatePayload(publicKey, signed, self.prefix)  
        return payload

    def notify_down(self, writer, reader):
        # receive public key, (ip, port), nonce
        signed=util.signWithKey(privateKey, ip, port, downIp, downPort)
        pass
        
    def notify_new_node(self, writer, reader):
        # receive public key, (ip, port, timestamp, order).signed, nonce (simple pow)
        signed-util.signWithKey(privateKey, ip, port, newNodeIp, newNodePort)
        pass

    def gossip(self, writer, reader):
        # command: NEW_NODE, DOWN, VALIDATE
        # receive public key, (ip, port, timestamp, order).signed, nonce (simple pow), command
        pass
