class Client:

    def __init__(self, client_id: int, client_name: str):
        self.client_id = client_id
        self.client_name = client_name

    # create a class takes in a dictionary and creates a client with that info
    def convert_dict(self, **d):
        pass

    def as_json_dict(self):
        return f"clientID: {self.client_id}, clientName: {self.client_name}"
