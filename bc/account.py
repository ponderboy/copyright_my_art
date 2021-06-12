# Wallet (quasi Account)
# id: Hash bzw. Wallet-Adresse
# coins: Guthaben, default: 0

class Account:

    def __init__(self, id):

        self.id = id
        self.coins = 0