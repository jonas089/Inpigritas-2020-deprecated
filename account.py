from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # RSA algorithm to sign with priv & verify with pub
from Crypto.Hash import SHA384
import hashlib, time, os, values, pickle

# C_Local : Local Blockchain
# B: Current Block

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
		Address = str(sha.hexdigest())
		return Address
		# Address is a hash representation of the string of the publickey => this ensures nobody can create a fake transaction by
		# using somebody else's Address combined with his own publickey => if Address != pubkey hashed : return False


#################################################################################################################################


def LoadBalance(address):
	Balance = 0.0
	Unconfirmed_Balance = 0.0
	with open('src/blockchain.dat', 'rb') as ChainFile:
		C_Local = pickle.load(ChainFile)
	# Fetch balance from local blockchain
	for Block in range(0, len(C_Local)):
		for Transaction in range(0, len(C_Local[Block]['transactions'])):
			if C_Local[Block]['transactions'][Transaction]['sender'] == address:
				Balance -= C_Local[Block]['transactions'][Transaction]['amount']
			if C_Local[Block]['transactions'][Transaction]['recipient'] == address:
				Balance += C_Local[Block]['transactions'][Transaction]['amount']

	# calculate interest // might be flawed
	Eligible_Interest = 0.0
	for B in range(0, len(C_Local)):
		# For every block 'B'
		for Tx_In_Block in range (0, len(C_Local[B]['transactions'])):
			# For every Transaction in 'B'
			if C_Local[B]['transactions'][Tx_In_Block]['sender'] == address:
				Eligible_Interest -= C_Local[B]['transactions'][Tx_In_Block]['amount']
			# Substract outgoing transaction(s) in Block
			elif C_Local[B]['transactions'][Tx_In_Block]['recipient'] == address:
				Eligible_Interest += C_Local[B]['transactions'][Tx_In_Block]['amount']
			# Incoming Transactions are eligible for Interest => added to Eligible_Interest
			elif C_Local[B]['transactions'][Tx_In_Block]['recipient'] == address and C_Local[B]['transactions'][Tx_In_Block]['sender'] == address:
				Eligible_Interest += 0.0
			# No Interest if Transaction is coming from the same wallet

		if Eligible_Interest > 0.0:
			# Add Interest to Eligible_Interest ( for current Block 'B' ).
			Eligible_Interest += Eligible_Interest * values.interest_per_block
	Balance = Eligible_Interest
	# !!!! Don't get mislead by Eligible_Interest - it stores the Balance with the Interest, not just the Interest. !!!!

	# calculate unconfirmed Balance ( from current block tx file )
	try:
		with open('src/TxBlockNo' + '000' + str(C_Local[len(C_Local) - 1]['index'] + 1) + '.dat', 'rb') as Block_Transaction_File:
			Block_Transactions_Unconfirmed = pickle.load(Block_Transaction_File)
		for uftx in range(0, len(Block_Transactions_Unconfirmed) - 1):
			if Block_Transactions_Unconfirmed[uftx]['sender'] == address:
				Unconfirmed_Balance -= Block_Transactions_Unconfirmed[uftx]['amount']
			if Block_Transactions_Unconfirmed[uftx]['recipient'] == address:
				Unconfirmed_Balance += Block_Transactions_Unconfirmed[utfx]['amount']
	except Exception as notransactions:
		print('[WARNING] NO TRANSACTION FILE FOUND FOR FOLLOWING BLOCK')

	Balances = [Balance, Unconfirmed_Balance]
	return Balances

def __Start__():
	# Check if wallet file exists, if not, create empty wallet.
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
	# For a new wallet, a new address needs to be generated. As of now, Inpigritas only support 1 address per 1 wallet.
	if new_wallet == True:
		Keys.Generate_Keypair()
		Addresses = [Keys.Generate_Address()]
		print('[NEW ADDRESS]' + Addresses[0])
		open('keys/account.dat', 'x')
		with open('keys/account.dat', 'wb') as account_file:
			pickle.dump(Addresses, account_file)
	else:
		return
