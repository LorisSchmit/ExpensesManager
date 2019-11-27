class Transaction:
    def __init__(self, date, type, sender, reference, amount, currency, tag):
        self.date = date
        self.type = type
        self.reference = reference
        self.sender = sender
        self.amount = amount
        self.currency = currency
        self.tag = tag