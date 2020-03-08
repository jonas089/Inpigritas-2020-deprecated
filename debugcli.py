import argparse
import chain
import validation
import account


parser = argparse.ArgumentParser(description='AMPS')
parser.add_argument('--newacc', '-na', dest='newacc',
	action = 'store_true')
parser.add_argument('--generategenesis', '-gg', dest='gengen',
	action = 'store_true')
parser.add_argument('--generateblock', '-gb', dest='genblo',
	action = 'store_true')
parser.add_argument('--help', '-h', dest='help')
parser.add_argument('--balance', '-b', dest='bal',
	action = 'store_true')

args = parser.parse_args()

if args.newacc:
	account.__Start__()
if args.help:
	print("""
	Help --> --help or -h
	New Account --> --newacc or -na
	Generate Genesis --> --generategenesis or -gg
	Generate Block --> --generateblock or -gb
	Balance --> --balance or -b
	""")
if args.gengen:
	LocalChain = chain.LOADLOCALCHAIN()
	if chain.LOCALCHAIN.BLOCKCHAINDAT() == True:
		chain.GENERATEGENESIS()

if args.genblo:
	dummytx = []
	LocalChain = chain.LOADLOCALCHAIN()
	chain.BLOCKCHAIN.BLOCK(LocalChain, dummytx)

if args.bal:
	print(account.LoadBalance())
