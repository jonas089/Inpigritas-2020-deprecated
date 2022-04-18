import argparse, chain, validation, account, transaction, requests, values, pickle

parser = argparse.ArgumentParser(description='AMPS')
parser.add_argument('--newacc', '-na', dest='newacc',
	action = 'store_true')
parser.add_argument('--generategenesis', '-gg', dest='gengen',
	action = 'store_true')
parser.add_argument('--generateblock', '-gb', dest='genblo',
	action = 'store_true')
parser.add_argument('--balance', '-b', dest='bal',
	action = 'store_true')
parser.add_argument('--transaction', '-tx', dest='transaction',
	action = 'store_true')

args = parser.parse_args()
if args.newacc:
	account.__Start__()
if args.gengen:
	LocalChain = chain.LOADLOCALCHAIN()
	if chain.LOCALCHAIN.BLOCKCHAINDAT() == True:
		chain.GENERATEGENESIS()
if args.genblo:
	dummytx = []
	LocalChain = chain.LOADLOCALCHAIN()
	chain.BLOCKCHAIN.BLOCK(LocalChain, dummytx)
if args.bal:
	with open('keys/account.dat', 'rb') as AccountFile:
		address = pickle.load(AccountFile)[0]
	Balances = account.LoadBalance(address)
	print('Confirmed: ' + str(Balances[0]) + '\n' + 'Unconfirmed: ' + str(Balances[1]))
if args.transaction:
	recipient = input('Recipient: ')
	amount = input('Amount: ')
	with open('keys/account.dat', 'rb') as AccountFile:
		address = pickle.load(AccountFile)[0]
	transaction.Transactions.CreateTransaction(recipient, float(amount))
