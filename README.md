# spinozacoin
a python-based blockchain

# Setting up
1. git clone https://github.com/larry94555/spinozacoin
2. pip install pyyaml
3. pip install cryptography
4. pip install typing
5. pip install tinyec
6. update spinozacoin.yml based on your set up (typically found in ~/spinozacoin/config/)
7. mkdir ~/spinozacoin/log

# Run
python spinozacoind.py (found in ~/spinozacoin/src/init)

# Plan

This project is an attempt to implement to implement an alternative blockchain to bitcoin and ethereum.  It is an attempt to create a complete ecosystem with sample applications.

I will be implmenting this project in phases:

Current Status:  **Phase 0**

* **Phase 1**:  Node discovery:  Provide a peer-to-peer network for nodes governed by a shared node directory of all validated nodes.
* **Phase 2**:  Blockchain:  Provide a blockchain that runs on top of the peer-to-peer network.  
* **Phase 3**:  Smart Contracts:  Provide a layer on top of blockchain to support smart contracts.
* **Phase 4**:  Currency:  Provide a currency that supports smart contracts and blockchain transactions
* **Phase 5**:  Application Ecosystem:  An ecoystem/infrastructure for providing web3 services and applications to consumers that run on the ecosyste
* **Phsae 6**:  Sample Applications:  At this point, I will start writing applications and services that can serve as samples of what cna be done using the ecosystem  
