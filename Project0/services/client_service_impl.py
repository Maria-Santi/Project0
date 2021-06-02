from daos.client_dao import ClientDAO
from entities.client import Client
from services.client_service import ClientService


class ClientServiceImpl(ClientService):

    def __init__(self, client_dao: ClientDAO):
        self.client_dao = client_dao

    def add_client(self, client: Client):
        return self.client_dao.create_client(client)

    def retrieve_all_clients(self):
        return self.client_dao.get_all_clients()

    def retrieve_client_by_id(self, client_id: int):
        return self.client_dao.get_client_by_id(client_id)

    def update_client(self, client_id: int, client: Client):
        return self.client_dao.update_client(client_id, client)

    def remove_client(self, client_id: int):
        return self.client_dao.delete_client(client_id)
