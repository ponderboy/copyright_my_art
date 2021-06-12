class Node:
    """
    Eine Node einer Blockchain bzw. eines P2P-Netzwerks
    """

    def __init__(self, address, account):

        self.address = address
        self.account = account