import hashlib
import time

LocalChain = []
TxData = []
blocktime = 10

class BLOCKCHAIN:
    def BLOCK():
        #[DEFINE BLOCKVARs FOR __GENESIS__ BLOCK]
        if len(LocalChain) == 0:
            is_genesis = True
            index = 0
            prev_hash = ''
        #[DEFINE BLOCKVARs FOR __BLOCK__ ]
        else:
            if time.time() < LocalChain[len(LocalChain) - 1]['next_timestamp']:
                return False
            is_genesis = False
            #[BLOCKVAR] 1                                   index
            index = len(LocalChain)
            #[BLOCKVAR] 2                                   prev_hash
            prev_hash = LocalChain[len(LocalChain) - 1]['block_hash']
        if is_genesis == True:
        #[BLOCKVAR] 3                                       timestamp
            timestamp = time.time()
        #[BLOCKVAR] 4                                       next_timestamp
            next_timestamp = timestamp + blocktime
        else:
            timestamp = LocalChain[len(LocalChain) - 1]['next_timestamp']
            next_timestamp = timestamp + blocktime
            #[HASHING]
        sha = hashlib.sha256()
        current_block_data_string = str(index) + prev_hash
        current_block_hash_string = sha.update(current_block_data_string.encode('utf-8'))
        #[BLOCKVAR] 5                                       block_hash
        block_hash = str(sha.hexdigest())
        sha = hashlib.sha256()
        next_block_data_string = str(index + 1) + block_hash
        next_block_hash_string = sha.update(next_block_data_string.encode('utf-8'))
        #[BLOCKVAR] 6                                       next_block_hash
        next_block_hash = str(sha.hexdigest())
            #[END OF HASHING]
        #[END OF BLOCKVAR DEFINITION]

#[CREATE BLOCK AS DICTIONARY]
        Block = {
        'index' : index,
        'prev_hash' : prev_hash,
        'timestamp' : timestamp,
        'next_timestamp' : next_timestamp,
        'block_hash' : block_hash,
        'next_block_hash' : next_block_hash
        }
#[END OF BLOCK DICTIONARY]
        LocalChain.append(index)
        LocalChain[index] = Block
        return True


#[CALL FUNCTIONS FOR TESTING || DEBUG]
for routine in range(0, 50): # Blocktime was changed to 10 seconds ==> running 50 times with a sleep timer will generate 5 Blocks
    BLOCKCHAIN.BLOCK()
    time.sleep(1)
for block in range(0, len(LocalChain)):
    print('[BLOCK]' + '\n' + '----------' + '\n' + str(LocalChain[block]) + '\n' + '---------' + '\n')
#[END OF DEBUGGING SECTION]
