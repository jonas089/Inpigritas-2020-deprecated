import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # / RSA algorithm to sign with priv(1) & verify with pub(1)
from Crypto.Hash import SHA384
import hashlib
import account

import pickle

class Transactions:
	def CreateTransaction(recipient, amount):