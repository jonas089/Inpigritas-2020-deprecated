[Version]: [Development V.0.0.0-00001]

Notes: The folder "DebugEnv" contains the current stable release x2
with two nodes preconfigured & two different accounts generated for 
testing. Enjoy this new, simple way to setup an Environment for further
investigation :)

############################################
#How to setup with two nodes (amps & amps2)#
############################################

- open cmd

[cmd] - cd /amps

- open another cmd(=cmd2)

[cmd2] - cd /amps2

[cmd] - python3 node.py -p 5000

[cmd2] - python3 node.py -p 5001

*blocks should be generated in both cmd-instances now*

############################################
#	Transactions                           #
############################################
starting balance: [amps]: 10,000,000 AMPS
		  [amps2]: 0.00 AMPS
wallet address [amps]:
eaedda3d0c197ce87076e7dfbbe00f344ffc3dddacea8747f7939f844f2b8a71bd814d147c0ab7cff014dc9a37292405

wallet address [amps2]:
2cfa2a14fd3e6ed405e23581833cd40e71512be0eb010f3e2a5e0578c8301ada62215758ba3f4e4b7ec19ea3640653c8

How to execute a transaction:

- open a third cmd(=cmd3)

[cmd3] - cd /amps
[cmd3] - python3 debugcli.py --transaction
	-> recipient: ENTER wallet address [amps2]
	-> amount: Any Integer or Float value that doesn't exceed you'r account balance
[cmd3] - cd ../amps2
[cmd3] - py debugcli.py --balance 
*it may or may not take another block to apply transactions & display the correct balance*