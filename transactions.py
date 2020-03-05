import hashlib
from Crypto.PublicKey import RSA
#from Crypto.Cipher import PKCS1_OAEP   # / RSA algorithm to encrypt with pub(2) & decrypt with priv(2)
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA256

mempool = []

class Transaction:
	def GENESIS_TRANSACTION():
		with open('keys/public_key.pem', 'r') as public_key_file:
			imported_public_key = RSA.importKey(public_key_file.read())
			exported_public_key = imported_public_key.exportKey('PEM')

		with open('keys/private_key.pem', 'r') as private_key_file:
			imported_private_key = RSA.importKey(private_key_file.read())
		amount = 1000.25 # Testing Amount for Premine
		recipient = '0'
		

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
#		assert verification, print('Error in Block verification')#return False