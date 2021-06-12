# account: Wallet-Adresse (anonym) - der public_key
# private_key - private Schlüssel für Zugriff auf Wallet

class User:

    def __init__(self, name, account, private_key):

        self.name = name
        self.account = account
        self.private_key = private_key