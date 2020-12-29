import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # RSA algorithm to sign with priv & verify with pub
from Crypto.Hash import SHA384
import hashlib
import time
import values
import pickle

class Keys:
	# Generates Keypair And Saves Both PRIVATE and PUBLIC KEY to your LOCAL Drive
	def Generate_Keypair(passwd=None): # added functionality for password protection (private key), will make default in the future
		key = RSA.generate(2048)
		try:
			os.mkdir('keys/')
		except Exception as exists:
			pass
		try:
			open('keys/private_key.pem', 'x')
		except Exception as exists:
			pass
		try:
			open('keys/public_key.pem', 'x')
		except Exception as exists:
			pass

		with open('keys/private_key.pem', 'wb') as private_key_file:
			private_key_file.write(key.exportKey('PEM', passphrase=passwd))
			private_key_file.close()
		with open('keys/public_key.pem', 'wb') as public_key_file:
			public_key_file.write(key.publickey().exportKey('PEM'))
			public_key_file.close()

	def Export_Pubkey():
		with open('keys/public_key.pem', 'r') as public_key_file:
			pubkey_pem = public_key_file.read()#pubkey.exportKey('PEM')
			return pubkey_pem

	def Import_Pubkey():
		with open('keys/public_key.pem', 'r') as public_key_file:
			pubkey = RSA.importKey(public_key_file.read())
			return pubkey

	def Import_Privkey(passwd=None): # added functionality for password protection (private key), will make default in the future
		with open('keys/private_key.pem', 'r') as private_key_file:
			privkey = RSA.importKey(private_key_file.read(), passphrase=passwd)
			return privkey

	def Generate_Address():
		publickey = Keys.Import_Pubkey()
		Address_data_string = str(publickey)
		sha = hashlib.sha384()
		Address_hash = sha.update(Address_data_string.encode('utf-8'))
		Address_hash_hex = sha.hexdigest()
		Address = str(Address_hash_hex)
		return Address
		# Address is a hash representation of the string of the publickey => this ensures nobody can create a fake transaction by
		# using somebody else's Address combined with his own publickey => if Address != pubkey hashed : return False

def LoadBalance(address):
	Balance = 0.0
	Unconfirmed_Balance = 0.0
	with open('src/blockchain.dat', 'rb') as ChainFile:
		LocalBlockChain = pickle.load(ChainFile)

	for Block in range(0, len(LocalBlockChain)):
		for Transaction in range(0, len(LocalBlockChain[Block]['transactions'])):
			if LocalBlockChain[Block]['transactions'][Transaction]['sender'] == address:
				Balance -= LocalBlockChain[Block]['transactions'][Transaction]['amount']
			if LocalBlockChain[Block]['transactions'][Transaction]['recipient'] == address:
				Balance += LocalBlockChain[Block]['transactions'][Transaction]['amount']

	# calculate interest
	Interest = 0.0
	block_balance = 0.0

	for Block_In_Chain in range(0, len(LocalBlockChain)):
		for TxInBlock in range (0, len(LocalBlockChain[Block_In_Chain]['transactions'])):
			if LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['sender'] == address:
				block_balance -= LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['amount']
			elif LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['recipient'] == address:
				block_balance += LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['amount']
			elif LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['recipient'] == address and LocalBlockChain[Block_In_Chain]['transactions'][TxInBlock]['sender'] == address:
				block_balance += 0.0
		if block_balance > 0.0:
			Interest = block_balance * values.interest_per_block
			block_balance += Interest
	Balance = block_balance
	next_index = LocalBlockChain[len(LocalBlockChain) - 1]['index'] + 1
	try:
		with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Block_Transaction_File:
			Block_Transactions_Unconfirmed = pickle.load(Block_Transaction_File)
		for uftx in range(0, len(Block_Transactions_Unconfirmed) - 1):
			if Block_Transactions_Unconfirmed[uftx]['sender'] == address:
				Unconfirmed_Balance -= Block_Transactions_Unconfirmed[uftx]['amount']
			if Block_Transactions_Unconfirmed[uftx]['recipient'] == address:
				Unconfirmed_Balance += Block_Transactions_Unconfirmed[utfx]['amount']
	except Exception as notransactions:
		print('[WARNING] NO TRANSACTION FILE FOUND FOR FOLLOWING BLOCK')
	Balances = []
	Balances.append(0)
	Balances.append(1)
	Balances[0] = Balance
	Balances[1] = Unconfirmed_Balance

	return Balances

def __Start__():
	new_wallet = False
	try:
		open('keys/private_key.pem', 'x')
		new_wallet = True
	except Exception as exists:
		pass
	try:
		open('keys/public_key.pem', 'x')
		new_wallet = True
	except Exception as exists:
		pass
	if new_wallet == True:
		Keys.Generate_Keypair()
		Addresses = []
		Addresses.append(0)
		Addresses[0] = str(Keys.Generate_Address())
		print('[NEW ADDRESS]' + Addresses[0])
		open('keys/account.dat', 'x')
		with open('keys/account.dat', 'wb') as account_file:
			pickle.dump(Addresses, account_file)
	else:
		return
