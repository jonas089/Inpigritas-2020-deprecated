####################################################################
#The apinode.py server handles API calls sent by the mobile client #
####################################################################

####################################################################
#                  Reference Version Code                          #
####################################################################
[V.0.0.0] This file only contains latest changes as of this version
####################################################################
#                       NEW FEATURES                               #
####################################################################

I.
[Accounting]

  @app.route => Generate_Cardholder_Account() requires two variables
                                                                    - tier
                                                                    - password
  tier describes the card-tier e.g.(gold, platinum, ...) [YET NOT NECESSARY]
  password is defined as developer_password.TXT and the linked hash is hardcoded
           is a validation implemented to avoid "card-account-creation-spamming"
           is required to ensure only developers can create new NFC-tagged Cardholder accounts
  Generate_Cardholder_Account() will RETURN only the ADDRESS !
  The Address will be written on a card and charged with an amount of coins manually depending on its tier
  The coins used to charge the Address (the Cardholder account) come from the DeveloperWallet [so to say "premine"]
  Transactions can be executed by using the card with the official mobile client
  [SECURITY NOTES]
    Every NearFieldContact generated Transaction has to be validated through the mobile app of the card-user,
    otherwise illegal transactions could be generated using the address of the cardholder.
    To link the Address generated for the NFC card and the owners Mobile-Account securely,
    the privateKey, which is stored on the APInode.py running server will be given to the Card-owner as login-information
  [KNOWN SECURITY ISSUES]
    Having the PrivateKey on the APIserver means the NFC / mobile accounts will be CENTRALIZED
    => SOLUTION: Recommandation to leave large holdings on a DECENTRALIZED PC-Wallet
      => Mobile wallet won't be insecure, but in theory remote-access to our APIserver could potentially leak the private-key
      [THIS HAS TO BE PREVENTED AS BEST AS POSSIBLE ON LAUNCH]
      Private key with password will probaly help solving this security-gap
        [IDEA] Card will be delivered with login data for mobile-client
               - username = ADDRESS
               - password = PASSWORD LINKED TO PRIVATE_KEY
        [END OF IDEA]
  [END OF KNOWN SECURITY ISSUES]
II.
[History]
  Returns Transaction-History for ANY ADDRESS

III.
[NFC-Transaction]
  def NFCtx(sender, recipient, string_amount, passwd=None):
  creates an NFC-Transaction from given parameters
