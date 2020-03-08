import requests
import chain
import json
import argparse

seeds = ['http://127.0.0.1:5000/',
        'http://127.0.0.1:5001/',
        'http://127.0.0.1:5002/']

def syncpeers():
    chain = chain.LOADLOCALCHAIN()
    for seed in seeds:
        nodeurl = seed + 'blockchain.json'
        print(nodeurl)
        try:
            nodechain = requests.get(nodeurl)
            chainjson = nodechain.json()[0]
            if len(chainjson) > len(chain):
                last_index_node_chain = len(chainjson) - 1
                last_index_local_chain = len(chain) - 1
                index_diff = last_index_node_chain - last_index_local_chain
                for b in range(len(chain), len(chainjson) - 1):
                    Block = chainjson[b]
                    if chain.BLOCKCHAIN.BLOCK(Block, chain) == False:
                        print('[E] [S1]')
                        return False
        except Exception as Networkerror:
            print(Networkerror)
