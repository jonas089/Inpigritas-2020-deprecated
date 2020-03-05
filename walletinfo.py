import os
from Crypto.PublicKey import RSA

class Keys:
	# Generates Keypair And Saves Both PRIVATE and PUBLIC KEY to your LOCAL Drive
	def Generate_Keypair():
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
			private_key_file.write(key.exportKey('PEM'))
			private_key_file.close()
		with open('keys/public_key.pem', 'wb') as public_key_file:
			public_key_file.write(key.publickey().exportKey('PEM'))
			public_key_file.close()
Keys.Generate_Keypair()

def GenerateAddress():
	with open('keys/pubkey.pem', 'r') as pubFile:
		pubkey = pubFile.read()
	sha = hashlib.sha384()
	Address_hash = sha.update(str(pubkey))
	Address = str(sha.hexdigest())
	return Address
