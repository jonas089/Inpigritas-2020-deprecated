from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import argparse
import account
import chain
import json
import sync

sched = BackgroundScheduler(standalone=True)
node = Flask(__name__)
account.__Start__()

@node.route('/blockchain.json', methods = ['GET'])
def ReturnLocalBlockchain():
  BlockChain = chain.LOADLOCALCHAIN()
  return BlockChain
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
    parser = argparse.ArgumentParser(description='AMPS Node')
    parser.add_argument('--port', '-p', default='5000',
                    help='port')
    parser.add_argument('--sync', '-s', dest='synchronize',
        action = 'store_true')
    args = parser.parse_args()
    node.run(host='127.0.0.1', port=args.port)
    if args.synchronize:
        sched.add_job(sync.syncpeers())
        sched.start()

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
