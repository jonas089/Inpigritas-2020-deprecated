import requests
import chain as c_hain
import json
import argparse

seeds = ['http://127.0.0.1:5000/',
        'http://127.0.0.1:5001/',
        'http://127.0.0.1:5002/']

def syncpeers():
    chain = c_hain.LOADLOCALCHAIN()
    for seed in seeds:
        nodeurl = seed + 'blockchain.json'
        print(nodeurl)
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
                        print('[E] [S1]')
                        return False
        except Exception as Networkerror:
            print(Networkerror)

    print(str(chainjson))
