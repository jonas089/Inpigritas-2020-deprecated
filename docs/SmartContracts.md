### DEPLOY A PYTHON SMARTCONTRACT with "debugcli.py"
* cd ./ (Inpigritas Root Directory)
* python3 debugcli.py --transaction
* INPUT --> Recipient
* INPUT --> Amount
* INPUT --> y/n ("y" if you want to deploy a contract)
* INPUT --> YOURSMARTCONTRACT.py (file needs to be placed in the Inpigritas Root Directory)
* DONE; CONTRACT ADDED TO TRANSACTIONPOOL; IT WILL BE DEPLOYED ONCE THE NEXT BLOCK HAS BEEN CONFIRMED

### GET ALL YOU'R PYTHON SMART CONTRACTS with "debugcli.py"
* cd ./ (Inpigritas Root Directory)
* python3 debugcli.py --all-contracts
* INPUT --> Contract_Owner_Address
* DONE; ALL CONTRACTS DEPLOYED BY THE GIVEN ADDRESS SHOULD BE PRINTED TO THE CONSOLE

### GET A SPECIFIC CONTRACT BY IT'S TRANSACTION's HASH with "debugcli.py"
* cd ./ (Inpigritas Root Directory)
* python3 debugcli.py --get-contract
* INPUT --> Contract_Transaction_Hash
* INPUT --> Contract_Owner_Address
* DONE; SPECIFIC CONTRACT's PYTHON CODE SHOULD BE PRINTED TO THE CONSOLE
