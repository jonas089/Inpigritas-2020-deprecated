import os, hashlib, account, pickle, requests, values, time, json, base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA384
import chain as c_hain

def Add_Transaction_Local(valid_transaction):
	fist_block_transaction = False
	height = valid_transaction['height']
	try:
		open('src/TxBlockNo' + '000' + str(height) + '.dat', 'x')
		fist_block_transaction = True
	except Exception as exists:
		fist_block_transaction = False
	if fist_block_transaction == True:
		BlockTxData = []
		BlockTxData.append(0)
		BlockTxData[0] = valid_transaction
		with open('src/TxBlockNo' + '000' + str(height) + '.dat', 'wb') as BlockTx_File:
			pickle.dump(BlockTxData, BlockTx_File)
			return True
	with open('src/TxBlockNo' + '000' + str(height) + '.dat', 'rb') as BlockTx_File_Backup:
		backup = pickle.load(BlockTx_File_Backup)
		index = len(backup)
		backup.append(index)
		backup[index] = valid_transaction
	with open('src/TxBlockNo' + '000' + str(height) + '.dat', 'wb') as BlockTx_File:
		pickle.dump(backup, BlockTx_File)
	return True

class Transactions:
	def Submit_Transaction_Network(transaction):
		seeds = values.seeds
		validations = 0
		for peer in seeds:
			nodeurl = peer
			print(nodeurl)
			try:
				nodechain = requests.get(nodeurl + 'blockchain.json')
				chainjson = nodechain.json()['data']
				chain = c_hain.LOADLOCALCHAIN()
				if len(chainjson) >= len(chain):
					transaction['height'] = len(chainjson)
					try:
						r = requests.post(peer + 'transaction', json=transaction)#json.dumps(transaction)))
						if r.text == 'False':
							print('[TRANSACTION GOT REJECTED BY NETWORK]')
							return False
						if r.text == 'True':
							validations += 1
						else:
							print('[UNKNOWN SERVER RESPONSE] : ' + str(r))
					except Exception as Network:
						print('[RESPONSE ERROR] : ' + str(Network))
						pass
			except Exception as Networkerror:
				print('[WARNING] NODE OFFLINE' + '\n' + str(Networkerror) + '\n')
		if validations >= values.required_validations:
			Add_Transaction_Local(transaction)
			return True
		else:
			return False
	def CreateTransaction(recipient, amount): # recipient is the string of an address
		with open('keys/account.dat', 'rb') as AddressFile:
			#[TXVAR]
			sender = pickle.load(AddressFile)[0]
		timestamp = time.time()
		#[TXVAR]
		pubkey_export = account.Keys.Export_Pubkey()
		pubkey_import = account.Keys.Import_Pubkey()
		privkey_import = account.Keys.Import_Privkey()
											#[TXVAR]	#[TXVAR]		#[TXVAR]
		transaction_data_string = sender + recipient + str(amount) + str(timestamp) + str(pubkey_export)
		sha = hashlib.sha384()
		transaction_hash = sha.update(transaction_data_string.encode('utf-8'))
		transaction_hash_hex = sha.hexdigest()
		#[TXVAR]
		transaction_hash_string = str(transaction_hash_hex)
		sigf = SHA384.new()
		sigf.update(str(timestamp).encode('utf-8'))
		transaction_cipher = PKCS1_v1_5.new(privkey_import)
		#[TXVAR]
		signature = transaction_cipher.sign(sigf)
		signature_export_b64 = base64.b64encode(signature)
		signature_export = signature_export_b64.decode('utf-8')
		print(signature)
		print(signature_export)
		transaction = {
			'sender' : sender,
			'recipient' : recipient,
			'timestamp' : timestamp,
			'amount' : amount,
			'publickey' : pubkey_export,
			'transaction_hash' : transaction_hash_string,
			'signature' : signature_export,
			'height' : int
		}
		Transactions.Submit_Transaction_Network(transaction)
