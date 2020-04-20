import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 # RSA algorithm to sign with priv & verify with pub
from Crypto.Hash import SHA384
import hashlib
import time
import values
import pickle

class Keys:

	# Generates Keypair And Saves Both PRIVATE and PUBLIC KEY to your LOCAL Drive
    def Generate_Keypair(passwd=None): # added functionality for password protection (private key), will make default in the future
        key = RSA.generate(2048)
        publickey = key.publickey()
        cardID = Keys.Generate_Address(publickey)
        try:
            os.mkdir('apidata/' + cardID)
        except Exception as exists:
            pass
        try:
            open('apidata/' + cardID + '/account.dat', 'x')
        except Exception as Exists:
            pass
        with open('apidata/' + cardID + '/account.dat', 'wb') as address_file:
            addresses = []
            addresses.append(0)
            addresses[0] = cardID
            pickle.dump(addresses, address_file)
        try:
            os.mkdir('keys/')
        except Exception as exists:
            pass
        try:
            open('apidata/' + cardID + '/private_key.pem', 'x')
        except Exception as exists:
            pass
        try:
            open('apidata/' + cardID + '/public_key.pem', 'x')
        except Exception as exists:
            pass
        with open('apidata/' + cardID + '/private_key.pem', 'wb') as private_key_file:
            private_key_file.write(key.exportKey('PEM', passphrase=passwd))
            private_key_file.close()
        with open('apidata/' + cardID + '/public_key.pem', 'wb') as public_key_file:
            public_key_file.write(key.publickey().exportKey('PEM'))
            public_key_file.close()
        return addresses[0]

    def Export_Pubkey(cardID):
        with open('apidata/' + cardID + '/public_key.pem', 'r') as public_key_file:
            pubkey_pem = public_key_file.read()#pubkey.exportKey('PEM')
            return pubkey_pem
    def Import_Pubkey(cardID):
        with open('apidata/' + cardID + '/public_key.pem', 'r') as public_key_file:
            pubkey = RSA.importKey(public_key_file.read())
            return pubkey
    def Import_Privkey(passwd=None): # added functionality for password protection (private key), will make default in the future
        with open('apidata/' + cardID + '/private_key.pem', 'r') as private_key_file:
            privkey = RSA.importKey(private_key_file.read(), passphrase=passwd)
            return privkey
    def Generate_Address(publickey):
        Address_data_string = str(publickey)
        sha = hashlib.sha384()
        Address_hash = sha.update(Address_data_string.encode('utf-8'))
        Address_hash_hex = sha.hexdigest()
        Address = str(Address_hash_hex)
        return Address
		# Address is a hash representation of the string of the publickey => this ensures nobody can create a fake transaction by
		# using somebody else's Address combined with his own publickey

def __Start__():
    cardID = ''
    return(Keys.Generate_Keypair())
