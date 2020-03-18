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
import values

def CHECKPOINTS():
	checkpoints = []
	checkpoints.append(0)
	checkpoints[0] = {}
	checkpoints[0]['index'] = 0
	checkpoints[0]['hash'] = '3e347d9058c0f117aa512f463d633b94069a9ce61d49df5a40b8348df41a03f3bd7cc1ffbeaf5da3c4c0c9f844e49265' # insert Genesis hash
	checkpoints[0]['next_hash'] = '250d8d8089db83f6d5556efcdaf0ed40041174ce5a7ccc6ad8af67a61ec61c0a3e564b756f3ed0f5aab2cdca866430d4' # insert Hash following Genesis hash
	checkpoints[0]['transactions'][0]['recipient'] = 'eaedda3d0c197ce87076e7dfbbe00f344ffc3dddacea8747f7939f844f2b8a71bd814d147c0ab7cff014dc9a37292405' # insert developer address receiving CAmount_Subsidy
	checkpoints[0]['transactions'][0]['amount'] = values.CAmount_Subsidy
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
			# comment out when generating genesis block
			if len(transactions) != 1:
				return False
			# comment out when generating genesis block
			if transactions[0]['recipient'] != genesis_checkpoint['transactions'][0]['recipient']:
				return False
			# comment out when generating genesis block
			if transactions[0]['amount'] != genesis_checkpoint['transactions'][0]['amount']:
				return False
			# comment out when generating genesis block
			if block_hash != genesis_checkpoint['hash']:
				return False
			# comment out when generating genesis block
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
		if len(Block['transactions']) != 0:
			for __transaction in range(0, len(Block['transactions']) - 1):
				if ValidationClass.VALIDATE_TRANSACTION(Block['transactions'][__transaction]) == False:
					print('[E] V6')
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
		sigf = SHA384.new()
		sigf.update(str(timestamp).encode('utf-8'))
		public_key = RSA.importKey(publickey)
		cypher = PKCS1_v1_5.new(public_key)
		verification = cypher.verify(sigf, signature)
		if verification == False:
			print('[E] [TV1]')
			return False
		if Balance < amount:
			print('[E] [TV2]')
			return False
		if amount <= 0.0:
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
		# Validate Transaction is not a Duplicate
		with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Block_Transaction_File:
			Block_Transactions_Unconfirmed = pickle.load(Block_Transaction_File)
			if tx in Block_Transactions_Unconfirmed:
				print('[E] [TV5]')
				return False
		with open('src/blockchain.dat', 'rb') as BlockChainFile:
			Total_Local_Chain = pickle.load(BlockChainFile)
			for fullblock in Total_Local_Chain:
				if tx in fullblock['transactions']:
					print('[E] [TV6]')
					return False
		print('[TRANSACTION ACCEPTED]')
		transaction.Add_Transaction_Local(tx)
		return True
