from validation import *
import hashlib
import time
import pickle

LocalChain = []
TxData = []
blocktime = 10

def LOADLOCALCHAIN():
    try:
        with open('data/blockchain.dat', 'rb') as chaindatafile:
            LocalChainLoaded = pickle.load(chaindatafile)
    except Exception as NoChain:
        LocalChainLoaded = []
    return LocalChainLoaded



class LOCALCHAIN:
    def BLOCKCHAINDAT():
        try:
            open('src/blockchain.dat', 'x')
            return True
        except Exception as Exists:
            return False

class BLOCKCHAIN:
    def BLOCK(transactions):
        #[DEFINE BLOCKVARs FOR __GENESIS__ BLOCK]
        if len(LocalChain) == 0:
            is_genesis = True
            index = 0
            prev_hash = ''
        #[DEFINE BLOCKVARs FOR __BLOCK__ ]
        else:
            if time.time() < LocalChain[len(LocalChain) - 1]['next_timestamp']:
                print('[E] [C1]')
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
        sha = hashlib.sha384()
        current_block_data_string = str(index) + prev_hash + str(timestamp)
        current_block_hash_string = sha.update(current_block_data_string.encode('utf-8'))
        #[BLOCKVAR] 5                                       block_hash
        block_hash = str(sha.hexdigest())
        sha = hashlib.sha384()
        next_block_data_string = str(index + 1) + block_hash + str(next_timestamp)
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
        'next_block_hash' : next_block_hash,
        'transactions' : transactions
        }
#[END OF BLOCK DICTIONARY]
        if ValidationClass.VALIDATE_BLOCK(Block, LocalChain, blocktime) == True:
            LocalChain.append(index)
            LocalChain[index] = Block
            with open('src/blockchain.dat', 'wb') as chaindatafile:
                pickle.dump(LocalChain, chaindatafile)
                print('[NEW BLOCK]' + str(Block))
        else:
            return False

        return True

def GENERATEGENESIS():
    CAmount_Subsidy = 2 * 1000 * 1000 * 1000 # 2 Billion for testing
    transactions = [{'sender' : '0', 'recipient' : '<DEVELOPER ADDRESS>', 'amount' : CAmount_Subsidy}]
    # the transaction data of the genesis block represents the premine
    while len(LocalChain) == 0:
        BLOCKCHAIN.BLOCK(transactions)
    print('[GENESIS]' + '\n' + '-' * 30 + '\n' + str(LocalChain) + '\n' + '-' * 30 + '\n')
    with open('src/blockchain.dat', 'wb') as chaindatafile:
        pickle.dump(LocalChain, chaindatafile)

    print('[GENESIS BLOCK] : ' + str(LocalChain[0]))
