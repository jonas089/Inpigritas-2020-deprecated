import requests
import chain as c_hain
import json
import argparse
import validation
import values
import threading
import time

blocktime = 10

seeds = values.seeds



def log_backup():
    with open('debug.log', 'r') as log_backup:
        backup = log_backup.read()
        return backup

def log_write(text):
    with open('debug.log', 'w') as log:
        log.write(text)

def newblock():
    dummytx = []
    LocalChain = c_hain.LOADLOCALCHAIN()
    c_hain.BLOCKCHAIN.BLOCK(LocalChain, dummytx)

def syncpeers(seeds_offline):
    try:
        open('src/blockchain.dat', 'x')
    except Exception as exists:
        pass
    print('[SYNCING]')
    seeds_total = len(seeds)
    for seed in seeds:
        nodeurl = seed + 'blockchain.json'
        #print(nodeurl)
        #log_write(log_backup() + '\n' + nodeurl)
        try:
            nodechain = requests.get(nodeurl)
            chainjson = nodechain.json()['data']
            chain = c_hain.LOADLOCALCHAIN()
            if len(chainjson) > len(chain):
                last_index_node_chain = len(chainjson)
                last_index_local_chain = len(chain) - 1
                index_diff = last_index_node_chain - last_index_local_chain
                for b in range(len(chain), len(chainjson)):
                    chain = c_hain.LOADLOCALCHAIN()
                    Block = chainjson[b]
                    #print(Block)
                    validation.ValidationClass.VALIDATE_BLOCK(Block, chain, values.blocktime)
                    #if validation.ValidationClass.VALIDATE_BLOCK(Block, chain, values.blocktime) == False:
                    #    log_write(log_backup() + '\n' + '[ERROR] INVALID BLOCK')
                    #    return False
        except Exception as Networkerror:
            #log_write(log_backup() + '\n' + '[WARNING] NODE OFFLINE' + '\n' + str(Networkerror) + '\n')
            seeds_offline += 1
    if seeds_offline >= seeds_total:
        print('[WARNING] SEEDS OFFLINE : ' + str(seeds_offline))
    else:
        log_write(log_backup() + '\n' + '[BLOCKS FETCHED AND ACCEPTED] :' + '\n' + str(chainjson))
        newblock()
        #syncpeers()
def sync_thread(process_var):
    while True:
        print('[SYNC PROCESS INITIATED]')
        seeds_offline = 0
        syncpeers(seeds_offline)
    #threading.Thread(target=syncpeers(), args=(), kwargs={}).start()
    #yield ('[DONE]')
