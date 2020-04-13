import requests

blocktime = 60 # 1 minute
CAmount_Subsidy = 10*1000*1000 # 10 million
Launch_Supply = 100 * 1000 * 1000 # 100 million
interest_per_block = 5 / 100 / 525600 # 5 percent per 525600 blocks == 1 year
rpc = 48937
port = ':48937'
ip = '0.0.0.0' # flask ip
dev_address = ''
external_ip = str(get('https://api.ipify.org').text)

seeds = ['127.0.0.1']
blacklisted_nodes = ['0.0.0.0', '127.0.0.1', 'localhost']
invalid_nodes = []

required_validations = 1
