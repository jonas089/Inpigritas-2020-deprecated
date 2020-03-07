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
class Validation:
	def VALIDATE_BLOCK(Block):

	def VALIDATE_TRANSACTION(Transaction):