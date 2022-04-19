import requests, json, argparse, validation, values, threading, time, pickle, os
import chain as c_hain

blocktime = values.blocktime
seeds = values.seeds

def log_backup():
    with open('debug.log', 'r') as log_backup:
        return log_backup.read()
def log_write(text):
    with open('debug.log', 'w') as log:
        log.write(text)

def fetch_pending_transactions():
    seeds_total = len(seeds)
    for seed in seeds:
        nodeurl = seed + 'txpool.json'
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
                nodetxpool = requests.get(seed + 'txpool.json')
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
    for seed in seeds:
        blacklist = values.blacklist
        if seed not in blacklist:
            try:
                nodechain = requests.get(seed + 'blockchain.json')
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
    # In case no Node is reachable
    if seeds_offline >= seeds_total:
        print('[WARNING] SEEDS OFFLINE : ' + str(seeds_offline))
    # If at least one valid node was found
    else:
        newblock()
def sync_thread(process_var):
    while True:
        print('[SYNC PROCESS INITIATED]')
        seeds_offline = 0
        syncpeers(seeds_offline)
