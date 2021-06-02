class Account:

    def __init__(self, account_id: int, client_id: int, category: str, balance: int):
        self.client_id = client_id
        self.account_id = account_id
        self.category = category
        self.balance = balance

    def convert_dict(self):
        pass

    def as_json_dict(self):
        return f"accountID: {self.account_id}, clientID: {self.client_id}, category: {self.category}, " \
               f"balance: {self.balance}"
