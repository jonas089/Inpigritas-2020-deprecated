from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from account import *
from chain import *
sched = BackgroundScheduler(standalone=True)

node = Flask(__name__)

account.__Start__()



@node.route('/blockchain.json', methods = ['GET'])
def ReturnLocalBlockchain():
  BlockChain = chain.LOADLOCALCHAIN()
  return BlockChain
@node.route('/block', methods=['POST'])
def ReceiveBlock():

@node.route('/transaction', methods=['POST'])
def ReceiveTransaction():







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

#if __name__ == '__main__':
#  parser = argparse.ArgumentParser(description='AMPS Node')
#  parser.add_argument('--port', '-p', default='5000',
#                    help='port')
#  parser.add_argument('--mine', '-m', dest='mine', 
#					action='store_true')
#  args = parser.parse_args()
#  if args.mine:
#  	sched.add_job(mine.minefromprev())
#  sched.start()
#  node.run(host='127.0.0.1', port=args.port)