import requests
import chain as c_hain
import json
import argparse
import validation
import values
import threading
import time
import pickle

blocktime = values.blocktime
seeds = seeds


def log_backup():
    with open('debug.log', 'r') as log_backup:
        backup = log_backup.read()
        return backup
def log_write(text):
    with open('debug.log', 'w') as log:
        log.write(text)

def fetch_pending_transactions():
    seeds_total = len(seeds)
    for seed in seeds:
        nodeurl = "http:" + seed + port + '/txpool.json'
        local_txpool = []
        LocalChain = c_hain.LOADLOCALCHAIN()
        try:
            next_index = LocalChain[len(LocalChain) - 1]['index'] + 1
        except Exception as GenesisBlockIndex:
            next_index = 0
        if next_index > 0:
            try:
                open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'x')
                with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'wb') as Dump_Empty:
                    pickle.dump(local_txpool, Dump_Empty)
            except Exception as block_includes_transactions:
                with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Transaction_Data_File:
                    local_txpool = pickle.load(Transaction_Data_File)
            try:
                nodetxpool = requests.get(nodeurl)
                txpooljson = nodetxpool.json()['data']
                chain = c_hain.LOADLOCALCHAIN()
                if len(txpooljson) > len(local_txpool):
                    local_txpool = txpooljson
                    for _tx in range(0, len(local_txpool)):
                        validation.VALIDATE_TRANSACTION(local_txpool[_tx])
                    print('[TXPOOL SYNCED]')
            except Exception as Networkerror:
                pass
        else:
            pass


def newblock():
    fetch_pending_transactions()# this is important in case the node has been booted up between two
                                # blocks when there are already transactions submitted to other nodes
    tx_data = []
    LocalChain = c_hain.LOADLOCALCHAIN()
    if time.time() < LocalChain[len(LocalChain) - 1]['next_timestamp']:
        return False
    next_index = LocalChain[len(LocalChain) - 1]['index'] + 1
    try:
        open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'x')
        with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'wb') as Dump_File:
            pickle.dump(tx_data, Dump_File)

    except Exception as block_includes_transactions:
        with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Transaction_Data_File:
            tx_data = pickle.load(Transaction_Data_File)
    c_hain.BLOCKCHAIN.BLOCK(LocalChain, tx_data)

def syncpeers(seeds_offline):
    try:
        open('src/blockchain.dat', 'x')
    except Exception as exists:
        pass
    print('[SYNCING]')
    seeds_total = len(seeds)
    all_seeds = seeds.append(values.external_ip)
    payload = {'peers': str(seeds)}
    for seed in seeds:
        if seed in values.blacklisted_nodes:
            continue
        nodeurl = "http://" + seed + values.port + '/blockchain.json'
        try:
            requests.post(seed, params=payload)
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
                    validation.ValidationClass.VALIDATE_BLOCK(Block, chain, values.blocktime)
        except Exception as Networkerror:
            print(str(Networkerror))
            seeds_offline += 1
            #values.invalid_nodes += seed
    if seeds_offline >= seeds_total:
        seeds.remove(seed) #this doesn't work, you can look into it, otherwise I'll fix it the next time :)
        print('[WARNING] SEEDS OFFLINE : ' + str(seeds_offline))
    else:
        #Memory Error detected: log_write takes too much RAM at certain hight
        #log_write(log_backup() + '\n' + '[BLOCKS FETCHED AND ACCEPTED] :' + '\n' + str(chainjson))
        newblock()
def sync_thread(process_var):
    while True:
        print('[SYNC PROCESS INITIATED]')
        seeds_offline = 0
        syncpeers(seeds_offline)
