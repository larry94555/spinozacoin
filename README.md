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
    * **Goal**: Reliable, Efficient Broadcasts across registered nodes in good standing
* **Phase 2**:  Blockchain:  Provide a blockchain that runs on top of the peer-to-peer network.
*   * **Goal**: Reliable, Efficient Transactions across registered nodes in good standing  
* **Phase 3**:  Smart Contracts:  Provide a layer on top of blockchain to support smart contracts.
    * **Goal**: Reliable, Efficient, Validated mini apps across registered nodes in good standing where the programming language is Turing complete. 
* **Phase 4**:  Currency:  Provide a currency that supports smart contracts and blockchain transactions
    * **Goal 1**: An incentive system providing cost for running apps, doing transactions, and broadcast and providing benefit for hosting apps, hosting transactions, hosting broadcasts, and hosting history of all transactions.
    * **Goal 2**: A means for a virtual gold system ("spinoza coin") that is deflationary and grows in value over time (analogous to bitcoin), a virtual cash system ("token") that is stable enough that it should have little speculative value (unless invested in something else) and safe enough that the only penalty for holding if over time is opportunity costs.   
* **Phase 5**:  Application Ecosystem:  An ecoystem/infrastructure for providing web3 services and applications to consumers that run on the ecosystem
    * **Goal 1**: An system for hosting self-run services and infrastructures such as Web Apps, Exchanges, Funds, Orchestrations, etc. 
    * **Goal 2**: A tutorial/starter system for building apps, exchanges, funds, orchestrations, and other self-run services and infrastructures  
* **Phsae 6**:  Sample Applications:  At this point, I will start writing applications and services that can serve as samples of what cna be done using the ecosystem
    * **Goal 1**: Write a reference application that runs on the application ecosystem
    * **Goal 2**: Proivde an incentive system for an application lifecycle on this ecosystem which would include funding (ICO), prototyping (demo), team collaboration (development), release (app store), app support infrastructure (storage, tokenization, etc.) 
