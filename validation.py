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
import transaction

def CHECKPOINTS():
	checkpoints = []
	checkpoints.append(0)
	checkpoints[0] = {}
	checkpoints[0]['index'] = 0
	checkpoints[0]['hash'] = 'cb5ef28937988f7ee948521633b3846619889a19ef9300ad91f4e59bc146a86b18c030ec0333024b274e1800fd132316' # insert Genesis hash
	checkpoints[0]['next_hash'] = '1a50407afabb1a64d9e11dfbe15c327d90f6e97fda96fb1bea75a286085f100ee0f976e06ca00cfd05928787390c612a' # insert Hash following Genesis hash
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
			genesis_checkpoint = CHECKPOINTS()[0]
			if index != genesis_checkpoint['index']:
				return False
			if block_hash != genesis_checkpoint['hash']:
				return False
			if next_block_hash != genesis_checkpoint['next_hash']:
				return False
			block_data_string = str(index) + prev_hash + str(timestamp)
			sha = hashlib.sha384()
			reconstructed_block_hash = sha.update(block_data_string.encode('utf-8'))
			block_hash_hex = sha.hexdigest()
			block_hash_string = str(block_hash_hex)
			next_block_data_string = str(index + 1) + block_hash + str(timestamp + blocktime)
			if block_hash_string != block_hash:
				print('[E] V4')
				return False
			sha = hashlib.sha384()
			reconstructed_next_block_hash = sha.update(next_block_data_string.encode('utf-8'))
			next_block_hash_hex = sha.hexdigest()
			next_block_hash_string = str(next_block_hash_hex)
			if next_block_hash_string != next_block_hash:
				print('[E] V5')
				return False
			print('[ADDING GENESISBLOCK]')
			c_hain.SAVEVALIDBLOCK(LocalChain, Block)
			return True
		if len(Block['transactions']) != 0:
			for BlockTransaction in range(0, len(Block['transactions']) - 1):
				if ValidationClass.VALIDATE_TRANSACTION(Block['transactions'][BlockTransaction]) == False:
					print('[BLOCK REJECTED BECAUSE INVALID TRANSACTIONS WERE IDENTIFIED]')
					return False
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
		signature = base64.b64decode(signature_encoded)
		print(str(signature))
		Balance = account.LoadBalance(sender)
		LocalChain = c_hain.LOADLOCALCHAIN()
		next_index = LocalChain[len(LocalChain) - 1]['index'] + 1
		with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Block_Transaction_File:
			Block_Transactions_Unconfirmed = pickle.load(Block_Transaction_File)
		for uftx in range(0, len(Block_Transactions_Unconfirmed)):
			if Block_Transactions_Unconfirmed[uftx]['sender'] == sender:
				Balance -= Block_Transactions_Unconfirmed[uftx]['amount']
			if Block_Transactions_Unconfirmed[uftx]['recipient'] == sender:
				Balance += Block_Transactions_Unconfirmed[utfx]['amount']
		if amount <= 0.0:
			print('[E] [TV1]')
			return False
		sigf = SHA384.new()
		sigf.update(str(timestamp).encode('utf-8'))
		public_key = RSA.importKey(publickey)
		cypher = PKCS1_v1_5.new(public_key)
		verification = cypher.verify(sigf, signature)
		if verification == False:
			print('[E] [TV2]')
			return False
		if Balance < amount:
			print('[E] [TV3]')
			return False

		# Validate Transaction Hash
		transaction_hash_data = sender + recipient + str(amount) + str(timestamp) + str(publickey)
		# publickey has to be reimported to be used for validation process
		sha = hashlib.sha384()
		transaction_hash_reconstructed = sha.update(transaction_hash_data.encode('utf-8'))
		transaction_hash_reconstructed_string = str(sha.hexdigest())
		if transaction_hash_reconstructed_string != transaction_hash:
			print('[E] [TV4]')
			return False

		print('[TRANSACTION ACCEPTED]')
		transaction.Add_Transaction_Local(tx)
		return True
