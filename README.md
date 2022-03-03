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
1. Start bootstrapped, test nodes (nodes that are preregistered)

```
python bootstrap.py -nc 1000
```

2. Start client to initiate broadcast (a node that does not need to register)

```
python trusted_client.py
```

# Plan

This project is an attempt to implement to implement an alternative blockchain to bitcoin and ethereum.  It is an attempt to create a complete ecosystem with sample applications.

Coming Soon: White Paper on the 6 proposed phases: "Constructing a Mainstream, Decentralized, Self-run Application Ecosystem"

**Basic Idea**: This is proposed as an alternative to cryptocurrencies.  It builds on the ideas of bitcoin, ethereum, and alt-coins but seeks to provide an alternative that
is mainstream, public, and conducive to promoting self-run software services.  The major value proposition offered is mainstream-friendly, decentralized, and a user-opted level of privacy (where the trade-off is recoverability versus irrecoverability).  Details will be presented in the white paper.

I will be implmenting this project in phases and will write a white paper for each phase which I will post in draft:

Current Status:  **Phase 1: configure up to 3900 validateable bootstrapped, test nodes, still need to add validation to test_client, registration process coming soon, and right now only simulating happy path for bootstarpped nodes (will add down nodes and random nodes for capability to test resilience)**

* **Phase 1**:  Node discovery:  Provide a peer-to-peer network for nodes governed by a shared node directory of all validated nodes.
    * **Goal**: Validateable, Efficient Broadcasts across registered nodes in good standing
* **Phase 2**:  Blockchain with currency on demand:  Provide a blockchain that runs on top of the peer-to-peer network and supports unlimited, test currency.
*   * **Goal**: Validateable, Efficient Transactions across registered nodes in good standing  
* **Phase 3**:  Smart Contracts:  Provide a layer on top of blockchain to support smart contracts.
    * **Goal**: Reliable, Efficient, Validated mini apps across registered nodes in good standing where the programming language is Turing complete. 
* **Phase 4**:  Currency:  Provide a currency that supports smart contracts and blockchain transactions with support for coins, tokens, and process for generating both.
    * **Goal 1**: An incentive system providing cost for running apps, doing transactions, and broadcast and providing benefit for hosting apps, hosting transactions, hosting broadcasts, and hosting history of all transactions.
    * **Goal 2**: A means for a virtual gold system ("spinoza coin") that is deflationary and grows in value over time (analogous to bitcoin), a virtual cash system ("token") that is stable enough that it should have little speculative value (unless invested in something else) and safe enough that the only penalty for holding if over time is opportunity costs.   
* **Phase 5**:  Application Ecosystem:  An ecoystem/infrastructure for providing web3 services and applications to consumers that run on the ecosystem
    * **Goal 1**: An system for hosting self-run services and infrastructures such as Web Apps, Exchanges, Funds, Orchestrations, etc. 
    * **Goal 2**: A tutorial/starter system for building apps, exchanges, funds, orchestrations, and other self-run services and infrastructures  
* **Phase 6**:  Sample Self-Run, Decentralized Applications:  At this point, I will start writing applications and services that can serve as samples of what cna be done using the ecosystem
    * **Goal 1**: Write a reference self-run, decentralized application that runs on the application ecosystem
    * **Goal 2**: Proivde an incentive system for an application lifecycle on this ecosystem which would include funding (ICO), prototyping (demo), team collaboration (development), release (app store), app support infrastructure (storage, tokenization, etc.) 
