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
	def VALIDATE(Block_Chain):
		for block_index in range(0, len(Block_Chain) - 1):
			index = Block_Chain[block_index]['index']
			prev_hash = Block_Chain[block_index]['prev_hash']
			timestamp = Block_Chain[block_index]['timestamp']
			next_timestamp = Block_Chain[block_index]['next_timestamp']
			block_hash = Block_Chain[block_index]['block_hash']
			next_block_hash = Block_Chain[block_index]['next_block_hash']

			# validation of <block_hash>
			data_string = str(index) + prev_hash + str(timestamp)
			sha = hashlib.sha384()
			reconstructed_block_hash = sha.update(data_string.encode('utf-8'))
			reconstructed_block_hash_string = str(sha.hexdigest())
			if reconstructed_block_hash_string != block_hash:
				print('[E1]')
				return False

			# validation of <next_block_hash>
			next_data_string = str(index + 1) + block_hash + str(next_timestamp)
			sha = hashlib.sha384()
			reconstructed_next_block_hash = sha.update(next_data_string.encode('utf-8'))
			reconstructed_next_block_hash_string = str(sha.hexdigest())
			if reconstructed_next_block_hash_string != next_block_hash:
				print('[E2]')
				return False

			# validation of <index>
			if block_index == 0 and index != 0:
				# Genesis index invalid
				print('[E3]')
				return False

			if block_index > 0 and index > 0:
				if index != Block_Chain[block_index - 1]['index'] + 1:
					# Block index invalid
					print('[E4]')
					return False
		# when every block was confirmed, return True ==> chain is valid !
		# Genesis should probably be a checkpoint...
		return True