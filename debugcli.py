import argparse
from chain import *
from validation import *
from account import *


parser = argparse.ArgumentParser(description='AMPS')
parser.add_argument('--newacc', '-na', dest='newacc',
	action = 'store_true')
parser.add_argument('--generategenesis', '-gg', dest='gengen',
	action = 'store_true')
parser.add_argument('--generateblock', '-gb', dest='genblo',
	action = 'store_true')

parser.add_argument('--balance', '-b', dest='bal',
	action = 'store_true')

args = parser.parse_args()

if args.newacc:
	__Start__()

if args.gengen:
	LocalChain = LOADLOCALCHAIN()
	if LOCALCHAIN.BLOCKCHAINDAT() == True:
		GENERATEGENESIS()

if args.genblo:
	dummytx = []
	LocalChain = LOADLOCALCHAIN()
	BLOCKCHAIN.BLOCK(dummytx)

if args.bal:
	print(LoadBalance())
