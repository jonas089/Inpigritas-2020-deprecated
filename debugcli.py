import argparse
import chain
import validation
import account
import transaction
import requests
import values
import pickle
import transaction

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

parser.add_argument('--get-contract', '-gct', dest='getcontract',
	action= 'store_true')
parser.add_argument('--execute-contract', '-ect', dest='executecontract',
	action= 'store_true')

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
	print(account.LoadBalance(address))
if args.transaction:
	recipient = input('Recipient: ')
	amount = input('Amount: ')
	with open('keys/account.dat', 'rb') as AccountFile:
		address = pickle.load(AccountFile)[0]
	deploy_contract_check = input('Does This Transaction Deploy A Smart Contract?(y, n): ')
	if deploy_contract_check == 'y' or deploy_contract_check == 'Y':
		print('[You Decided To Deploy A Contract]')
		unique_contract_name = input('Enter Unique Contract Name: ')
		data = {}
		contract_python_file_name = input('Enter The Name Of The File That Contains The Contract You Want To Deploy (e.g. test.py): ')
		with open(contract_python_file_name, 'rb') as PythonContractFile:
			contract_bytes = PythonContractFile.read()
		data = {
		'owner_address' : address,
		'contract_code' : contract_bytes.decode('utf-8'),
		'unique_contract_name' : unique_contract_name,
		}
	else:
		print('[You Decided To NOT Deploy A Contract]')
		data = {
		'owner_address' : address,
		'contract_code' : '',
		'unique_contract_name' : '',
		}
	transaction.Transactions.CreateTransaction(recipient, float(amount), data)
if args.getcontract:
	unique_contract_name = input('Enter Contract Name: ')
	contract_owner_address = input('Enter Contract Owner Address: ')
	contract_code = account.GetContractFromChain(unique_contract_name, contract_owner_address)
	print(contract_code)
