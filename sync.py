import requests
import chain as c_hain
import json
import argparse
import validation

seeds = ['http://127.0.0.1:5000/',
        'http://127.0.0.1:5001/',
        'http://127.0.0.1:5002/']

def log_backup():
    with open('debug.log', 'r') as log_backup:
        backup = log_backup.read()
        return backup

def log_write(text):
    with open('debug.log', 'w') as log:
        log.write(text)

def syncpeers():
    chain = c_hain.LOADLOCALCHAIN()
    for seed in seeds:
        nodeurl = seed + 'blockchain.json'
        print(nodeurl)

        log_write(log_backup() + '\n' + nodeurl)

        try:
            nodechain = requests.get(nodeurl)
            chainjson = nodechain.json()['data']
            if len(chainjson) > len(chain):
                last_index_node_chain = len(chainjson)
                last_index_local_chain = len(chain) - 1
                index_diff = last_index_node_chain - last_index_local_chain
                for b in range(len(chain), len(chainjson) - 1):
                    Block = chainjson[b]
                    if c_hain.BLOCKCHAIN.BLOCK(Block, chain) == False:
                        log_write(log_backup() + '\n' + '[ERROR] INVALID BLOCK')
                        return False
        except Exception as Networkerror:
            log_write(log_backup() + '\n' + '[WARNING] NODE OFFLINE')

    log_write(log_backup() + '\n' + '[BLOCKS FETCHED AND ACCEPTED] :' + '\n' + str(chainjson))
