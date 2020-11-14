blocktime = 60 # 1 minute
CAmount_Subsidy = 10*1000*1000 # 10 million
interest_per_block = 5 / 100 / 525600 # 5 percent per 525600 blocks == 1 year
rpc = 5000
ip = '127.0.0.1'

seeds = [#'http://127.0.0.1:5000/',
        'http://127.0.0.1:5001/'#,
        #'http://127.0.0.1:5002/'
        ]
blacklist = []

required_validations = 1 #int(len(seeds/2)) + 1 #50% of nodes + 1

#########################################[Static Variables]######################################################
dev_address = '8e00ffcb8ed746401347d10acddb55e4a7c89ad097ff325e68f0ef62e1b6ae89293353c8e7bb919ffe1bdf3483149678'
genesis_hash = '9000eb6af19ba4e14af71efb9159883f40c24cdaa9c9d3882ad5e09732c60e3e4d51c4590ae7960eaf3c929ade9af770'
genesis_next_hash = '89f6c517f74e1e410b9058abed9abaeda715cde71b3185d2770526b484196c7e9477f03729b4b9afaae6f57089348118'
#################################################################################################################
