import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA384
# blockstructure : index, prev_hash, timestamp, next_timestamp, block_hash, next_block_hash
# blockvalues (hashed) : index, prev_hash, timestamp
import chain as c_hain
import account
import pickle
import base64

def CHECKPOINTS():
	checkpoints = []
	checkpoints.append(0)
	checkpoints[0] = {}
	checkpoints[0]['index'] = 0
	checkpoints[0]['hash'] = '' # insert Genesis hash
	checkpoints[0]['next_hash'] = '' # insert Hash following Genesis hash
	return checkpoints
class ValidationClass:
	def VALIDATE_BLOCK(Block, LocalChain, blocktime):
		index = Block['index']
		prev_hash = Block['prev_hash']
		timestamp = Block['timestamp']
		next_timestamp = Block['next_timestamp']
		block_hash = Block['block_hash']
		next_block_hash = Block['next_block_hash']
		transactions = Block['transactions']

		if index == 0:
			print('[ADDING GENESISBLOCK]')
			c_hain.SAVEVALIDBLOCK(LocalChain, Block)
			return True # >>> Add Genesis Validation as Checkpoint <<< #
		if index != len(LocalChain):
			print(index)
			print(len(LocalChain))
			print('[E] V1')
			return False
		if timestamp != LocalChain[len(LocalChain) - 1]['next_timestamp']:
			print('[E] V2')
			return False
		if block_hash != LocalChain[len(LocalChain) - 1]['next_block_hash']:
			print('[E] V3')
			return False
		block_data_string = str(index) + prev_hash + str(timestamp)
		sha = hashlib.sha384()
		reconstructed_block_hash = sha.update(block_data_string.encode('utf-8'))
		block_hash_hex = sha.hexdigest()
		block_hash_string = str(block_hash_hex)

		if block_hash_string != block_hash:
			print('[E] V4')
			return False

		next_block_data_string = str(index + 1) + block_hash + str(timestamp + blocktime)
		sha = hashlib.sha384()
		reconstructed_next_block_hash = sha.update(next_block_data_string.encode('utf-8'))
		next_block_hash_hex = sha.hexdigest()
		next_block_hash_string = str(next_block_hash_hex)

		if next_block_hash_string != next_block_hash:
			print('[E] V5')
			return False
		print('[ADDING BLOCK]')
		c_hain.SAVEVALIDBLOCK(LocalChain, Block)
		return True

	def VALIDATE_TRANSACTION(tx):
		sender = tx['sender']
		recipient = tx['recipient']
		timestamp = tx['timestamp']
		amount = tx['amount']
		publickey = tx['publickey']
		transaction_hash = tx['transaction_hash']
		signature_encoded = tx['signature'].encode('utf-8')
		siganture = base64.b64decode(signature_encoded)
		Balance = account.LoadBalance(sender)
		if Balance < amount:
			return False

		#######################################
		#	implement a balance check 		  #
		#######################################

		# Validate Transaction Hash
		transaction_hash_data = sender + recipient + str(amount) + str(timestamp) + str(publickey)
		# publickey has to be reimported to be used for validation process
		sha = hashlib.sha384()
		transaction_hash_reconstructed = sha.update(transaction_hash_data.encode('utf-8'))
		transaction_hash_reconstructed_string = str(sha.hexdigest())
		if transaction_hash_reconstructed_string != transaction_hash:
			print('[E] [TV1]')
			return False

		print('[EXTERNAL TRANSACTION ACCEPTED]')
		return True

#		transaction = {
#			'sender' = sender,
#			'recipient' = recipient,
#			'timestamp' = timestamp,
#			'amount' = amount,
#			'publickey' = pubkey_export,
#			'transaction_hash' = transaction_hash_string,
#			'signature' = signature
#			sender + recipient + str(amount) + str(timestamp) + str(pubkey_export)

#		genSHA = SHA256.new()
#		genSHA.update(blockhash.encode('utf-8'))
#		cypher = PKCS1_v1_5.new(pubkey)
#		verification = cypher.verify(genSHA, sig)
#		assert verification, print('Error in Block verification')		}
