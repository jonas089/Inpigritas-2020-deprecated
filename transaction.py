import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA384
import hashlib
import account
import pickle
import requests
import values
import time
import chain as c_hain
import json

import base64

class Transactions:
	def Submit_Transaction_Network(transaction):
		seeds = values.seeds
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
						#if r == False:
						#	return False
					except Exception as Network:
						print('[RESPONSE ERROR] : ' + str(Network))
						pass
			except Exception as Networkerror:
				print('[WARNING] NODE OFFLINE' + '\n' + str(Networkerror) + '\n')

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


		# pubkey_exported
		# signature
#[NOTES]
#			[SAMPLE FOR KEYS AND SIGNATURE]
#			with open('keys/public_key.pem' , 'r') as public_key_file:
#				public_key = RSA.importKey(public_key_file.read())
#				self.pubkey = public_key.exportKey('PEM')



#				hash_utf = self.hash.encode('utf-8')
#				with open('keys/private_key.pem', 'r') as privkey_File:
#					privkey = RSA.importKey(privkey_File.read())
#				genSHA = SHA256.new()
#				genSHA.update(hash_utf)
#				self.sigf = genSHA
#				unique_cipher = PKCS1_v1_5.new(privkey)
#				# genSHA=sigf
#				self.sig = unique_cipher.sign(genSHA)


#		genSHA = SHA256.new()
#		genSHA.update(blockhash.encode('utf-8'))
#		cypher = PKCS1_v1_5.new(pubkey)
#		verification = cypher.verify(genSHA, sig)
#		assert verification, print('Error in Block verification')
