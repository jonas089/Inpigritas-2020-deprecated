# Inpigritas Cryptocurrency

Proof of Δ Time (POΔT) consens algorithm

# The Flask-version of Inpigritas has been deprecated.
# Positive Conclusions:
Inpigritas-Flask (this repo) was an interesting project, as the network seems to be stable and the validations seem to do their job.
It is a secure way to submit transactions that are then hashed into a blockchain and can be validated by nodes within the Network.
# Negative Conclusions and issues worth considering in the future:
1. Building a blockchain in python is much more efficient and easier to work with when using classes for blocks. 
2. Flask is not fast enought to support the required amount of transactions per second for a decentralized transaction network of scale.
3. Linear growth, as there is no zsnarks or similar summarized blocks built in.
4. Inefficient storage of data ( using pickle over a database ), many temporary files that were not deleted properly. => loss of memory & storage
# General issues with Proof of deltatime:
1. Proof of deltatime turned out to not be suitable for a consens algorihm. Proof of elapsed time (INTEL) is a method of distribution for 
2. a decentralized currency, whilest Inpigritas implementation of a time-based blockchain requires a centralized entity to distribute coins from the 
0-address. there might be ways to implement automated, decentralized distribution through an on-chain distribution functionality, maybe in the form
of a smartcontract, but these changes have not been implemented in Inpigritas-Flask. Therfore Proof of Deltatime can not be considered an consens-algorithm
and 
## Inpigritas-Flask is therfore not a decentralized cryptocurreny.

In order to make Inpigritas a cryptocurrency that is worth being developed further, the following changes are 
# MANDATORY:
1. use sockets over flask.
2. code either a smartcontract or a similar on-chain solution to distribute Inpigritas to node-operators.
(maybe consider a temporary POW-solution to do further research)
3. improve storage and memory use + add checkpoints to the blockchain to improve efficiency.

# Inpigritas-Skeleton is currently the ongoing development repository for Inpigritas. Inpigritas-Flask ( this repo ) is DEPRECATED.
## Inpigritas-Flask will not be further developed.

# To be done
- restructure and improve the code, make it easier to work with
- improve filesystem / database and temporarly stored transaction data
- improve speed / light wallets or similar solution(s)
- regulate distribution of supply / for example by forking another coins chain
- improve / finish the web-interface and integrate a well documented API for integration of services

### Required libraries are in requirements.txt
### Virtualenv setup scripts included
## Debugging
 - debugshell.py; interactive shell for debugging
 - debugcli.py; pass arguments to execute functions for debugging
## Testing Environment Setup
- assuming 2 nodes with empty "src" and "keys" folder(s)

# DEVELOPMENT BUILD
## V.0.0.0

## Step 1:
 # In values.py
   Node#1
   port = 5000
   seeds = ['127.0.0.1:5001']

   Node#2
   port = 5001
   seeds = ['127.0.0.1:5000']
## Step 2:
   cd Node1
   py debugcli.py --newacc
   --> outputs account address ( referenced below as "Node1_Address")

   cd Node2
   py debugcli.py --newacc
   --> outputs account address
## Step 3:
 # In values.py
   dev_address = Node1_Address (see Readme.md line 21)
## Step 4:
 # In validation.py
 [THIS IS EXTREMELY IMPORTANT]
 [DO THIS ONLY FOR NODE 1 !]
   put a hashtag "#" in front of every line of code that is marked as "comment out when generating the genesis block"
## Step 5:
  cd Node1
  py debugcli.py --generategenesis
  --> outputs genesisblock data
## Step 6:
   copy-paste "src" folder from Node1 to Node2
   Revert Step 4 and remove all hashtags placed in that step
   replace "static" variables "genesis_hash" and "genesis_next_hash" with those who were output of Step 5
## Step 7:
   cd into Node 1 and execute:
   py node.py

   cd into Node 2 and execute:
   py node.py

   open a 3rd terminal and cd into Node 1 (premine located),
   then execute a transaction through debugclient as follows:
   py debugcli.py
   # INPUT
   --> amount
   --> recipient

   cd into Node 2 and execute:
   py node.py

   open a 3rd terminal and cd into Node 1 (premine located),
   then execute a transaction through debugclient as follows:
   py debugcli.py --transaction
   # INPUT
   --> amount
   --> recipient

TESTING ENVIRONMENT SETUP SUCCESSFUL IF TRANSACTION ACCEPTED BY NETWORK
