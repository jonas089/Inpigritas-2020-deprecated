from validate import *
import hashlib
import time
import pickle

LocalChain = []
TxData = []
blocktime = 10

class Localchain:
    def BLOCKCHAINDAT():
        try:
            open('data/blockchain.dat', 'x')
        except Exception as Exists:
            print(Exists)
            pass
    def WALLETDAT():
        try:
            open('data/wallet.dat', 'x')
        except Exception as Exists:
            print(Exists)
            pass

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
        current_block_data_string = str(index) + prev_hash + str(timestamp)
        current_block_hash_string = sha.update(current_block_data_string.encode('utf-8'))
        #[BLOCKVAR] 5                                       block_hash
        block_hash = str(sha.hexdigest())
        sha = hashlib.sha256()
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
        'next_block_hash' : next_block_hash
        }
#[END OF BLOCK DICTIONARY]
        LocalChain.append(index)
        LocalChain[index] = Block
        if Validation.VALIDATE(LocalChain) == True:
            with open('data/blockchain.dat', 'wb') as chaindatafile:
                pickle.dump(LocalChain, chaindatafile)
        else:
            return False

        return True

def GENERATEGENESIS():
    while len(LocalChain) == 0:
        BLOCKCHAIN.BLOCK()
    print('[GENESIS]' + '\n' + '-' * 30 + '\n' + str(LocalChain) + '\n' + '-' * 30 + '\n')
    with open('data/blockchain.dat', 'wb') as chaindatafile:
        pickle.dump(LocalChain, chaindatafile)


Localchain.BLOCKCHAINDAT()
Localchain.WALLETDAT()


#[CALL FUNCTIONS FOR TESTING || DEBUG]
debugI = input('[Genesis] = Generate Genesis Block; [Generate] = Generate 5 Blocks: ')
if debugI == 'Generate':
    with open('data/blockchain.dat', 'rb') as chaindatafile:
        LocalChain = pickle.load(chaindatafile)
    for routine in range(0, 50): # Blocktime was changed to 10 seconds ==> running 50 times with a sleep timer will generate 5 Blocks
        BLOCKCHAIN.BLOCK()
        time.sleep(1)
    for block in range(0, len(LocalChain)):
        print('[BLOCK]' + '\n' + '----------' + '\n' + str(LocalChain[block]) + '\n' + '---------' + '\n')
#[END OF DEBUGGING SECTION]
if debugI == 'Genesis':
    GENERATEGENESIS()