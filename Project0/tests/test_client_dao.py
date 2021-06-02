import pytest

from daos.client_dao import ClientDAO
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from exceptions.not_found_exception import ResourceNotFoundError

client_dao: ClientDAO = ClientDAOPostgres()

test_client = Client(0, "Evelyn")


def test_create_client():
    client_dao.create_client(test_client)
    assert test_client.client_id != 0


def test_get_client_by_id():
    client = client_dao.get_client_by_id(test_client.client_id)
    assert test_client.client_id == client.client_id


def test_get_client_by_id_exception():
    with pytest.raises(ResourceNotFoundError):
        client_dao.get_client_by_id(80)


def test_get_all_clients():
    clients = client_dao.get_all_clients()
    assert len(clients) >= 2


def test_update_client():
    test_client.client_name = "Olivia"
    client = client_dao.update_client(test_client.client_id, test_client)
    assert test_client.client_id == client.client_id


def test_update_client_exception():
    with pytest.raises(ResourceNotFoundError):
        test_client1 = Client(0, "Evelyn")
        client_dao.update_client(80, test_client1)


def test_delete_client():
    result = client_dao.delete_client(test_client.client_id)
    assert result


def test_delete_client_exception():
    with pytest.raises(ResourceNotFoundError):
        client_dao.delete_client(80)
