import hashlib, account, pickle, base64, transaction, values
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA384
# blockstructure : index, prev_hash, timestamp, next_timestamp, block_hash, next_block_hash
# blockvalues (hashed) : index, prev_hash, timestamp
import chain as c_hain

def CHECKPOINTS():
	checkpoints = []
	checkpoints.append(0)
	checkpoints[0] = {}
	checkpoints[0]['index'] = 0
	checkpoints[0]['hash'] = values.genesis_hash # insert Genesis hash
	checkpoints[0]['next_hash'] = values.genesis_next_hash # insert Hash following Genesis hash
	checkpoints[0]['recipient'] = values.dev_address # insert developer address receiving Premine
	checkpoints[0]['amount'] = values.Premine
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
				print('[E] VG1')
				return False
#			# comment out when generating genesis block
			if len(transactions) != 1:
				print('[E] VG2')
				return False
#			# comment out when generating genesis block
			if transactions[0]['recipient'] != genesis_checkpoint['recipient']:
				print('[E] VG3')
				return False
#			# comment out when generating genesis block
			if transactions[0]['amount'] != genesis_checkpoint['amount']:
				print('[E] VG4')
				return False
#			# comment out when generating genesis block
			if block_hash != genesis_checkpoint['hash']:
				print('[E] VG5')
				return False
#			# comment out when generating genesis block
			if next_block_hash != genesis_checkpoint['next_hash']:
				print('[E] VG6')
				return False
			block_data_string = str(index) + prev_hash + str(timestamp)
			sha = hashlib.sha384()
			reconstructed_block_hash = sha.update(block_data_string.encode('utf-8'))
			block_hash_hex = sha.hexdigest()
			block_hash_string = str(block_hash_hex)
			next_block_data_string = str(index + 1) + block_hash + str(timestamp + blocktime)
			if block_hash_string != block_hash:
				print('[E] V1')
				return False
			sha = hashlib.sha384()
			reconstructed_next_block_hash = sha.update(next_block_data_string.encode('utf-8'))
			next_block_hash_hex = sha.hexdigest()
			next_block_hash_string = str(next_block_hash_hex)
			if next_block_hash_string != next_block_hash:
				print('[E] V2')
				return False
			print('[ADDING GENESISBLOCK]')
			c_hain.SAVEVALIDBLOCK(LocalChain, Block)
			return True
		if index != len(LocalChain):
			print(index)
			print(len(LocalChain))
			print('[E] V3')
			return False
		if timestamp != LocalChain[len(LocalChain) - 1]['next_timestamp']:
			print('[E] V4')
			return False
		if block_hash != LocalChain[len(LocalChain) - 1]['next_block_hash']:
			print('[E] V5')
			return False
		block_data_string = str(index) + prev_hash + str(timestamp)
		sha = hashlib.sha384()
		reconstructed_block_hash = sha.update(block_data_string.encode('utf-8'))
		block_hash_hex = sha.hexdigest()
		block_hash_string = str(block_hash_hex)
		if block_hash_string != block_hash:
			print('[E] V6')
			return False
		next_block_data_string = str(index + 1) + block_hash + str(timestamp + blocktime)
		sha = hashlib.sha384()
		reconstructed_next_block_hash = sha.update(next_block_data_string.encode('utf-8'))
		next_block_hash_hex = sha.hexdigest()
		next_block_hash_string = str(next_block_hash_hex)
		if next_block_hash_string != next_block_hash:
			print('[E] V7')
			return False
		if len(Block['transactions']) != 0:
			for __transaction in range(0, len(Block['transactions'])):
				if ValidationClass.VALIDATE_TRANSACTION(Block['transactions'][__transaction]) == False:
					print('!-----[E] Type: "TV"-----!')
					return False
				LocalBlockChain = c_hain.LOADLOCALCHAIN()
				for __block in range(0, len(LocalBlockChain)):
					if __transaction in LocalBlockChain[__block]['transactions']:
						print('[E] [TVE0]')
						return False
				next_index = LocalBlockChain[len(LocalBlockChain) - 1]['index'] + 1
				with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Block_Transaction_File:
					Block_Transactions_Unconfirmed = pickle.load(Block_Transaction_File)
				for _ltx in range(0, len(Block['transactions'])):
					if __transaction != _ltx and Block['transactions'][__transaction] == Block['transactions'][_ltx]:
						print('[E] [TVE1]')
						return False
				with open('src/blockchain.dat', 'rb') as BlockChainFile:
					Total_Local_Chain = pickle.load(BlockChainFile)
					for fullblock in Total_Local_Chain:
						if __transaction in fullblock['transactions']:
							print('[E] [TVE2]')
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
		Balance = account.LoadBalance(sender)[0]
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
		print('[TRANSACTION ACCEPTED]')
		transaction.Add_Transaction_Local(tx)
		return True
