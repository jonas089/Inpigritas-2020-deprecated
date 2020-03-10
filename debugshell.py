import chain
import validation
import account
import transaction
import sys
import code
import pickle

def ahelp():
    print("""
    Generate Genesis --> gengen()
    New Account --> newacc()
    Generate Block --> genblo()
    Balance --> bal()
    """)

def gengen():
    LocalChain = chain.LOADLOCALCHAIN()
    if chain.LOCALCHAIN.BLOCKCHAINDAT() == True:
        chain.GENERATEGENESIS()

def newacc():
    account.__Start__()

def genblo():
    dummytx = []
    LocalChain = chain.LOADLOCALCHAIN()
    chain.BLOCKCHAIN.BLOCK(LocalChain, dummytx)

def bal():
    with open('keys/account.dat', 'rb') as AccountFile:
        address = pickle.load(AccountFile)[0]
    print(account.LoadBalance(address))

print("Use ahelp() for debug help and help() for python help!")
ahelp()

code.interact(local=locals())
