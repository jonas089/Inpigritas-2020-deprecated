from flask import Flask, request, jsonify, render_template
import argparse, account, chain, json, sync, pickle, threading, values, validation, time, transaction
from multiprocessing import Process, Value

node = Flask(__name__)
account.__Start__()

@node.route('/interface', methods = ['GET'])
def NodeInterface():
    return render_template('index.html')

@node.route('/iwallet', methods = ['GET'])
def IWallet():
    return render_template('wallet.html')

@node.route('/itransaction', methods=['POST'])
def ITransaction():
    recipient = request.form['recipient']
    # Amount has to be valid / e.g. not negative.
    try:
        amount = float(request.form['amount'])
    except Exception as Invalid_Amount:
        return 'Invalid Amount, Please Try Again'

    transaction.Transactions.CreateTransaction(request.form['recipient'], amount)
    return render_template('wallet.html')

@node.route('/blockchain.json', methods = ['GET'])
def ReturnLocalBlockchain():
    BlockChainDict = {
    'data':chain.LOADLOCALCHAIN()
    }
    return BlockChainDict

@node.route('/txpool.json', methods = ['GET'])
def ReturnTxPool():
    LocalChain = chain.LOADLOCALCHAIN()

    # Try to fetch next block index from localchain, if this fails, there is no transactions in the block (yet)
    try:
        next_index = LocalChain[len(LocalChain) - 1]['index'] + 1
    except Exception as NoChain:
        return {}
    # Fetch and Return the Transactionpool as a Dictionary ( unless empty )
    try:
        with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Transaction_Data_File:
            TransactionPoolDict = {
            'data':pickle.load(Transaction_Data_File)
            }
    except Exception as Empty:
        pass
    # Return the pending Transactions in the next Block to be "mined" as a Dictionary
    return TransactionPoolDict

@node.route('/block/<blkindex>', methods=['GET'])
def SendBlock(index):
    # Try to return the Block with "index"=index
    try:
        return chain.LOADLOCALCHAIN()[index]
    # No such block exists.
    except IndexError:
        return False

@node.route('/balance/<address>', methods=['GET'])
def WalletAmount(address):
    # Return the Confirmed Balance of the given Wallet address.
    return account.LoadBalance(address)[0]

@node.route('/transaction', methods=['POST'])
def ReceiveTransaction():
    print('[TRANSACTION RECEIVED] : [VALID = ' + str(validation.ValidationClass.VALIDATE_TRANSACTION(request.get_json())) + ' ]')
    return(str(validation.ValidationClass.VALIDATE_TRANSACTION(request.get_json())))

if __name__ == '__main__':
    print(r'''
╭━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮
╰┫┣╯╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╯╰╮
╱┃┃╱╭━╮╱╭━━╮╭╮╭━━╮╭━╮╭╮╰╮╭╯╭━━╮╭━━╮
╱┃┃╱┃╭╮╮┃╭╮┃┣┫┃╭╮┃┃╭╯┣┫╱┃┃╱┃╭╮┃┃━━┫
╭┫┣╮┃┃┃┃┃╰╯┃┃┃┃╰╯┃┃┃╱┃┃╱┃╰╮┃╭╮┃┣━━┃
╰━━╯╰╯╰╯┃╭━╯╰╯╰━╮┃╰╯╱╰╯╱╰━╯╰╯╰╯╰━━╯
╱╱╱╱╱╱╱╱┃┃╱╱╱╱╭━╯┃
╱╱╱╱╱╱╱╱╰╯╱╱╱╱╰━━╯
    ''')

    try:
        open('debug.log', 'x')
    except Exception as exists:
        pass

    parser = argparse.ArgumentParser(description='Inpigritas Node')
    parser.add_argument('--port', '-p', default=str(values.rpc),
                    help='port')
    args = parser.parse_args()
    process_var = Value('b', True)
    # this had to be moved above node.run as it otherwise only gets called when the connection breaks
    p = Process(target=sync.sync_thread, args=(process_var, ))
    p.start()
    node.run(threaded=True, host=values.ip, port=args.port, use_reloader=False)
    p.join()
