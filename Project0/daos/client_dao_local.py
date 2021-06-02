from typing import List

from daos.client_dao import ClientDAO
from entities.client import Client
from exceptions.not_found_exception import ResourceNotFoundError


class ClientDAOLocal(ClientDAO):
    client_id_maker = 0
    client_table = {}

    def create_client(self, client: Client) -> Client:
        ClientDAOLocal.client_id_maker += 1
        client.client_id = ClientDAOLocal.client_id_maker
        ClientDAOLocal.client_table[ClientDAOLocal.client_id_maker] = client
        return client

    def get_client_by_id(self, client_id: int) -> Client:
        try:
            client = ClientDAOLocal.client_table[client_id]
            return client
        except KeyError:
            raise ResourceNotFoundError(f"Client with id {client_id} could not be found")

    def get_all_clients(self) -> List[Client]:
        client_list = list(ClientDAOLocal.client_table.values())
        return client_list

    def update_client(self, client_id: int, client: Client) -> Client:
        try:
            if client_id in ClientDAOLocal.client_table.keys():
                ClientDAOLocal.client_table[client_id] = client
                return client
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client with id {client_id} could not be found")

    def delete_client(self, client_id: int) -> bool:
        try:
            del ClientDAOLocal.client_table[client_id]
            return True
        except KeyError:
            raise ResourceNotFoundError(f"Client with id {client_id} could not be found")
