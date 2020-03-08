from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import argparse
import account
import chain
import json
import sync
import pickle

sched = BackgroundScheduler(standalone=True)
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
    return True

@node.route('/transaction', methods=['POST'])
def ReceiveTransaction():
    transaction_decoded = request.data.decode('utf-8')
    transaction_jsonified = json.loads(transaction_decoded)
    print(transaction_jsonified)
    return True


if __name__ == '__main__':
    try:
        open('debug.log', 'x')
    except Exception as exists:
        pass


    parser = argparse.ArgumentParser(description='AMPS Node')
    parser.add_argument('--port', '-p', default='5000',
                    help='port')
    parser.add_argument('--sync', '-s', dest='synchronize',
        action = 'store_true')
    args = parser.parse_args()
    # this had to be moved above node.run as it otherwise only gets called when the connection breaks
    if args.synchronize:
        sched.add_listener(sync.syncpeers(), apscheduler.events.EVENT_JOB_EXECUTED)
    sched.start()
    print('running')
    node.run(host='127.0.0.1', port=args.port)

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
