from flask import Flask, request
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
node = Flask(__name__)
account.__Start__()

@node.route('/blockchain.json', methods = ['GET'])
def ReturnLocalBlockchain():
    BlockChain = chain.LOADLOCALCHAIN()
    BlockChainDict = {}
    BlockChainDict['data'] = BlockChain
    return BlockChainDict
@node.route('/block', methods=['POST'])
def ReceiveBlock():
    block_decoded = request.data.decode('utf-8')
    block_jsonified = json.loads(block_decoded)
    print(block_jsonified)
    return ('DONE')

#@node.route('/syncnetwork', methods=['GET'])
#def SyncNetwork():
#    sync.sync_thread()
#    return ('DONE')

@node.route('/transaction', methods=['POST'])
def ReceiveTransaction():
    transaction_decoded = request.data.decode('utf-8')
    transaction_jsonified = json.loads(transaction_decoded)
    print(transaction_jsonified)
    return ('DONE')

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

#  if args.mine:
#      sched.add_job(mine.minefromprev())
#      sched.start()

#@node.route('/potblock', methods = ['POST'])
#def ReceiveBlock():
#	print(request.data.decode('utf-8'))
#	time.sleep(2)
#	potblock_str = request.data#.decode('utf-8')
#	potblock = json.loads(request.data)
#	print(potblock)
#	if validate.validatePot(potblock) == True:
#		print("[VALID]")
#		return True
#	else:
#		print("[INVALID]")
#		return False
