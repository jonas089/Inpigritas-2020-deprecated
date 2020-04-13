import hashlib

password = input('Enter Password... ')

sha = hashlib.sha384()

sha.update(password.encode('utf-8'))

password_hash = sha.hexdigest()

print(password_hash)

input('Enter to Exit... ')