import hashlib
# blockstructure : index, prev_hash, timestamp, next_timestamp, block_hash, next_block_hash
# blockvalues (hashed) : index, prev_hash, timestamp
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

		return True

	def VALIDATE_TRANSACTION(Transaction):
		# there are 2 types of transactions
		# I. user to user
		# II. payment for staking
		sender = Transaction['sender']
		recipient = Transaction['recipient']
		amount = Transaction['amount']
		timestamp = Transaction['timestamp']
		signature = Transaction['signature']
		pubkey = Transaction['pubkey']
		
	def VALIDATE_STAKING(Stak):
