from flask import Flask, request, jsonify
import argparse
import account
import chain
import json
import sync
import pickle
import threading
import values
#from threading import Thread
from multiprocessing import Process, Value
import validation
from transaction import Transactions
import time
import code

def ahelp():
    print("""
    Generate Genesis --> gengen()
    New Account --> newacc()
    Generate Block --> genblo()
    Balance --> bal()
    Printchain --> printchain(index of block)
    Node --> startnode()
    Transaction --> transaction()
    """)

def printchain(num=0):
    array = chain.LOADLOCALCHAIN()
    print(array[num])


def gengen():
    LocalChain = chain.LOADLOCALCHAIN()
    if chain.LOCALCHAIN.BLOCKCHAINDAT() == True:
        chain.GENERATEGENESIS()

def newacc():
    account.__Start__()

def genblo():
    dummytx = []
    LocalChain = chain.LOADLOCALCHAIN()
    chain.BLOCKCHAIN.BLOCK(LocalChain, dummytx)

def bal():
    with open('keys/account.dat', 'rb') as AccountFile:
        address = pickle.load(AccountFile)[0]
    print(account.LoadBalance(address))

def transaction():
    recipient = input('Recipient: ')
    amount = input('Amount: ')
    Transactions.CreateTransaction(recipient, float(amount))


def startnode():
    node = Flask(__name__)
    account.__Start__()

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


print("Use ahelp() for debug help and help() for python help!")
ahelp()
code.interact(local=locals())
