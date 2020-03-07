from validate import *
import hashlib
import time
import pickle

LocalChain = []
TxData = []
blocktime = 10

def LOADLOCALCHAIN():
    try:
        with open('data/blockchain.dat', 'rb') as chaindatafile:
            LocalChain = pickle.load(chaindatafile)
            return LocalChain
    except Exception as NoChain:
        return LocalChain


class LOCALCHAIN:
    def BLOCKCHAINDAT():
        try:
            open('data/blockchain.dat', 'x')
        except Exception as Exists:
            print(Exists)
            pass

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
        print(transactions)

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
        LocalChain.append(index)
        LocalChain[index] = Block
        if Validation.VALIDATE(Block) == True:
            with open('data/blockchain.dat', 'wb') as chaindatafile:
                pickle.dump(LocalChain, chaindatafile)
        else:
            return False

        return True

def GENERATEGENESIS():
    transactions = []
    while len(LocalChain) == 0:
        BLOCKCHAIN.BLOCK(transactions)
    print('[GENESIS]' + '\n' + '-' * 30 + '\n' + str(LocalChain) + '\n' + '-' * 30 + '\n')
    with open('data/blockchain.dat', 'wb') as chaindatafile:
        pickle.dump(LocalChain, chaindatafile)

    print('[GENESIS BLOCK] : ' + str(LocalChain[0]))



GENERATEGENESIS()
LOCALCHAIN.BLOCKCHAINDAT()
LOADLOCALCHAIN()
#BLOCKCHAIN.BLOCK(<transaction>)
