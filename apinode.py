from flask import Flask, request, jsonify
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # RSA algorithm to sign with priv & verify with pub
from Crypto.Hash import SHA384
import hashlib
import base64
import time
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
import transaction as _tx


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

########################
#  ###### ##### #####  #
#  #    # #   #   #    #
#  ###### #####   #    #
#  #    # #       #    #
#  #    # #     #####  #
########################
@node.route('/api/balance/<address>', methods=['GET'])
def Api_Balance(address):
    return str(account.LoadBalance(address))

@node.route('/api/txhistory/<address>', methods=['GET'])
def Api_TxHistory(address):
    TxData = []
    TxData.append(0)
    TxData.append(1)
    TxData[0] = [] # processed incoming transcations
    TxData[1] = [] # processed outgoing transactions
    LocalBlockChain = chain.LOADLOCALCHAIN()
    for Block in range(0, len(LocalBlockChain)):
        for Transaction in range(0, len(LocalBlockChain[Block]['transactions'])):
            if LocalBlockChain[Block]['transactions'][Transaction]['sender'] == address:
                TxData[1].append(len(TxData[1]))
                TxData[1][len(TxData[1]) - 1] = LocalBlockChain[Block]['transactions'][Transaction]
            if LocalBlockChain[Block]['transactions'][Transaction]['recipient'] == address:
                TxData[0].append(len(TxData[0]))
                TxData[0][len(TxData[0]) - 1] = LocalBlockChain[Block]['transactions'][Transaction]
    return str(TxData)
@node.route('/nfcpayment/<sender>/<recipient>/<string_amount>', methods=['GET'])
def NFCtx(sender, recipient, string_amount, passwd=None):
    amount = float(string_amount)
    if sender not in values.dev_cards:
        return '[Error]'
    timestamp = time.time()
    #[TXVAR]
    with open('apidata/' + sender + '/public_key.pem', 'r') as public_key_file:
        pubkey_export = public_key_file.read()
    with open('apidata/' + sender + '/private_key.pem', 'r') as private_key_file:
        privkey_import = RSA.importKey(private_key_file.read(), passphrase=passwd)

    										#[TXVAR]	#[TXVAR]		#[TXVAR]
    transaction_data_string = sender + recipient + str(amount) + str(timestamp) + str(pubkey_export)
    sha = hashlib.sha384()
    transaction_hash = sha.update(transaction_data_string.encode('utf-8'))
    transaction_hash_hex = sha.hexdigest()
    #[TXVAR]
    transaction_hash_string = str(transaction_hash_hex)
    sigf = SHA384.new()
    sigf.update(str(timestamp).encode('utf-8'))
    transaction_cipher = PKCS1_v1_5.new(privkey_import)
    #[TXVAR]
    signature = transaction_cipher.sign(sigf)
    signature_export_b64 = base64.b64encode(signature)
    signature_export = signature_export_b64.decode('utf-8')
    print(signature)
    print(signature_export)
    transaction = {
    	'sender' : sender,
    	'recipient' : recipient,
    	'timestamp' : timestamp,
    	'amount' : amount,
    	'publickey' : pubkey_export,
    	'transaction_hash' : transaction_hash_string,
    	'signature' : signature_export,
    	'height' : int
    }
    return(str(_tx.Transactions.Submit_Transaction_Network(transaction)))

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
    node.run(threaded=True, host=values.ip, port=80, use_reloader=False)
    p.join()
