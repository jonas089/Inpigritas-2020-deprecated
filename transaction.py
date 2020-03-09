import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA384
import hashlib
import account
import pickle

class Transactions:
	def CreateTransaction(recipient, amount): # recipient is the string of an address
		with open('keys/account.dat', 'rb') as AddressFile:
			#[TXVAR]
			sender = pickle.load(AddressFile)[0]
		timestamp = time.time()
		#[TXVAR]
		pubkey_export = account.Export_Pubkey()
		pubkey_import = account.Import_Pubkey()
		privkey_import = account.Import_Privkey()
											#[TXVAR]	#[TXVAR]		#[TXVAR]
		transaction_data_string = sender + recipient + str(amount) + str(timestamp) + str(pubkey_export)
		sha = hashlib.sha384()
		transaction_hash = sha.update(transaction_data_string.encode('utf-8'))
		transaction_hash_hex = sha.hexdigest()
		#[TXVAR]
		transaction_hash_string = str(transaction_hash_hex)
		sigf = SHA384.new()
		sigf.update(timestamp.encode('utf-8'))
		transaction_cipher = PKCS1_v1_5.new(privkey_import)
		#[TXVAR]
		signature = transaction_cipher.sign(sigf)

		transaction = {
			'sender' : sender,
			'recipient' : recipient,
			'timestamp' : timestamp,
			'amount' : amount,
			'publickey' : pubkey_export,
			'transaction_hash' : transaction_hash_string,
			'signature' : signature
		}
		print('[TRANSACTION] : ' + str(transaction))
		return transaction
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
