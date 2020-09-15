# Inpigritas Cryptocurrency
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
