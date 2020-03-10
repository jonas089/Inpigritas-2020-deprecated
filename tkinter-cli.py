import tkinter as tk
import pickle
import account

root = tk.Tk()

is_address = False
is_balance = False
try:
    with open('keys/account.dat', 'rb') as Address_File:
        is_address = True
        wallet_address_zero = pickle.load(Address_File)[0]
        address_Label = tk.Label(root, text= '\n' + '[Address]' + '\n' + str(wallet_address_zero), bg='black', fg='white')
except Exception as exists:
    print('[WARNING] : ' + str(exists))
    is_address = False

try:
    is_balance = True
    with open('keys/account.dat', 'rb') as AccountFile:
        address = pickle.load(AccountFile)[0]
    balance = account.LoadBalance(address)
    balance_Label = tk.Label(root, text= '\n' + '[Balance]' + '\n' + str(balance), bg='black', fg='white')
except Exception as exists:
    print('[WARNING] : ' + 'Balance could not be retrieved')
    is_balance = False


header = tk.Label(root, text="    Ampere GUI Client    ", fg='white', font=("Helvetica", 20), bg='blue')
header.pack()
if is_address == True:
    address_Label.pack()
if is_balance == True:
    balance_Label.pack()
root.geometry("600x600")
root.mainloop()
