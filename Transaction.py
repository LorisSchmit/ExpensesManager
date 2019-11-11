class Transaction:
    def __init__(self, date, type, reference, recipient, amount, currency, tag):
        self.date = date
        self.type = type
        self.reference = reference
        self.recipient = recipient
        self.amount = amount
        self.currency = currency
        self.tag = tag