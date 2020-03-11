import chain
import validation
import account
import transaction
import sys
import code
import tkinter
import sync
from threading import Thread

def updateblockchain():
    Loaded = False
    while Loaded == Fale:
        try:
            with open('src/blockchain.dat', 'rb') as chaindatafile:
                LocalChainLoaded = pickle.load(chaindatafile)
                Loaded = True
        except Exception as NoChain:
            msg_list.insert("")
"""
def login():
    account.__Start__()
    account.Keys.
"""

my_msg=""
help = ("""
    help --> prints this message
    newacc (passwd) --> generate new account
    importacc --> login
    balance --> checks balance
    printaddress --> prints wallet address
    chain --> prints blockchain
    """)

def UI():
    top = tkinter.Tk()
    top.title("Ampere")
    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar() # variable that the input box stores stuff if in
    my_msg.set("Type your messages here!")
    scrollbar = tkinter.Scrollbar(messages_frame) # to navigate through past messages
    # following will contain messages
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    #entry_field.bind("<Return>", interpret(my_msg))
    entry_field.pack()
    #send_button = tkinter.Button(top, text="Send", command=interpret(my_msg))
    #send_button.pack()
    login_button = tkinter.Button(top, text="Login", command=login)
    login_button.pack()

    #makes the program more modular
    #serv_msg = tkinter.StringVar()
    #serv_msg.set("Enter server address here!")
    #serventry_field = tkinter.Entry(top, textvariable=serv_msg)
    #serventry_field.bind("<Return>", connect)
    #serventry_field.pack()

    #top.protocol("WM_DELETE_WINDOW", on_closing) # when window is closed execute on_closing

    #receive_thread = Thread(target=receive)
    #receive_thread.start()
    tkinter.mainloop()

UI()
