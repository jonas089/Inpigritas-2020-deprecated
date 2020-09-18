from sanic import Sanic
from sanic import response
from multiprocessing import Process, Value
from RestrictedPython import compile_restricted, safe_globals
import chain, argparse, account

app = Sanic(name="Inpigritas Node")

@app.route('/blockchain')
async def blockchain(request):
    LocalChain = chain.LOADLOCALCHAIN()
    BlockChainDict = {}
    BlockChainDict["Data"] = LocalChain
    return response.json(BlockChainDict)

@app.route('/txpool')
async def transactionpool(request):
    LocalChain = chain.LOADLOCALCHAIN()
    TransactionPoolDict = {}
    try:
        next_index = LocalChain[len(LocalChain) - 1]['index'] + 1
    except Exception as NoChain:
        return response.json(TransactionPoolDict)
    local_txpool = []
    try:
        with open('src/TxBlockNo' + '000' + str(next_index) + '.dat', 'rb') as Transaction_Data_File:
            local_txpool = pickle.load(Transaction_Data_File)
    except Exception as no_data:
        pass
    TransactionPoolDict['data'] = local_txpool
    return response.json(TransactionPoolDict)

@app.route('/block/<blocknum>')
async def returnblock(request, blocknum):
    array = chain.LOADLOCALCHAIN()
    try:
        block = array[int(blocknum)]
        return response.json(block)
    except IndexError:
        return response.text("False")

@app.route('/transaction')
async def receivetransaction(request):
    values = await request.json()
    result = validation.ValidationClass.VALIDATE_TRANSACTION(values)
=======
        return Falsemultidict==4.7.6
pycrypto==2.6.1
requests==2.24.0
RestrictedPython==5.0
rfc3986==1.4.0
sanic==20.6.3
sniffio==1.1.0

@node.route('/balance/<address>', methods=['GET']) # this isnt completely done
def WalletAmount(address):multidict==4.7.6
pycrypto==2.6.1
requests==2.24.0
RestrictedPython==5.0
rfc3986==1.4.0
sanic==20.6.3
sniffio==1.1.0
    balance = account.LoadBalance(address)
    return balance

    
@node.route('/transaction', methods=['POST'])
def ReceiveTransaction():
    #transaction_decoded = request.data.decode('utf-8')
    transaction_jsonified = request.get_json()#json.loads(request.data)
    #print(transaction_jsonified)
    result = validation.ValidationClass.VALIDATE_TRANSACTION(transaction_jsonified)

@app.route('/contract')
async def executecontract(request):
    values = await request.json()
    code = account.GetContractFromChain(contract_transaction_hash, owner_address)
    byte_code = compile_restricted(code, '<inline>', 'exec')
    exec(byte_code, safe_globals, {})
    return response.text(str({}))


app.run(host='0.0.0.0', port=8000, debug=True)
