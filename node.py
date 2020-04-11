from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import argparse
import account
import chain
import json
import sync
import pickle
import threading
import values
from multiprocessing import Process, Value
import validation

import time


node = Flask(__name__)
account.__Start__()
limiter = Limiter(
    node,
    key_func=get_remote_address,
    default_limits=["30 per minute"]
)

@node.route('/blockchain.json', methods = ['GET'])
def ReturnLocalBlockchain():
    BlockChain = chain.LOADLOCALCHAIN()
    BlockChainDict = {}
    BlockChainDict['data'] = BlockChain
    return BlockChainDict

@node.route('/txpool.json', methods = ['GET'])
def ReturnTxPool():
    LocalChain = chain.LOADLOCALCHAIN()
    TransactionPoolDict = {}
    try:
        next_index = LocalChain[len(LocalChain) - 1]['index'] + 1
    except Exception as NoChain:
        return TransactionPoolDict
    local_txpool = []
    try:
        with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Transaction_Data_File:
            local_txpool = pickle.load(Transaction_Data_File)
    except Exception as no_data:
        pass
    TransactionPoolDict['data'] = local_txpool
    return TransactionPoolDict

@node.route('/block/<blkindex>', methods=['GET'])
def SendBlock(blkindex):
    array = chain.LOADLOCALCHAIN()
    try:
        block = array[blkindex]
        return block
    except IndexError:
        return False

@node.route('/transaction', methods=['POST'])
def ReceiveTransaction():
    #transaction_decoded = request.data.decode('utf-8')
    transaction_jsonified = request.get_json()#json.loads(request.data)
    #print(transaction_jsonified)
    result = validation.ValidationClass.VALIDATE_TRANSACTION(transaction_jsonified)
    print('[TRANSACTION RECEIVED] : [VALID = ' + str(result) + ' ]')
    return(str(result))



if __name__ == '__main__':
    try:
        open('debug.log', 'x')
    except Exception as exists:
        pass

    parser = argparse.ArgumentParser(description='AMPS Node')
    parser.add_argument('--port', '-p', default=str(values.rpc),
                    help='port')
    args = parser.parse_args()
    process_var = Value('b', True)
    # this had to be moved above node.run as it otherwise only gets called when the connection breaks
    p = Process(target=sync.sync_thread, args=(process_var, ))
    p.start()
    node.run(threaded=True, host=values.ip, port=args.port, use_reloader=False)
    p.join()
