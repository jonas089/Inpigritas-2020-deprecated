blocktime = 60 # 1 minute
CAmount_Subsidy = 10*1000*1000 # 10 million
interest_per_block = 5 / 100 / 525600 # 5 percent per 525600 blocks == 1 year
rpc = 5000
ip = '127.0.0.1'

seeds = [#'http://127.0.0.1:5000/',
        'http://127.0.0.1:5001/',
        'http://127.0.0.1:5002/'
        ]
blacklist = []

required_validations = 1 #int(len(seeds/2)) + 1 #50% of nodes + 1

#########################################[Static Variables]######################################################
dev_address = 'eaedda3d0c197ce87076e7dfbbe00f344ffc3dddacea8747f7939f844f2b8a71bd814d147c0ab7cff014dc9a37292405'
genesis_hash = ''
genesis_next_hash = ''
#################################################################################################################
