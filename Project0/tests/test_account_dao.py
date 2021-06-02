import pytest

from daos.account_dao import AccountDAO
from daos.account_dao_postgress import AccountDAOPostgres
from daos.client_dao import ClientDAO
from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from entities.account import Account
from exceptions.not_found_exception import ResourceNotFoundError

account_dao: AccountDAO = AccountDAOPostgres()
client_dao: ClientDAO = ClientDAOPostgres()

test_client = Client(0, "Olivia")
client_dao.create_client(test_client)

test_account = Account(0, test_client.client_id, "Checking", 500)


def test_get_client_exists():
    c_exists = account_dao.get_client_exists(test_client.client_id)
    assert c_exists


def test_create_account():
    account_dao.create_account(test_client.client_id, test_account)
    assert test_account.account_id != 0


def test_account_belongs_to_client():
    a_exists = account_dao.get_account_belongs_to_client(test_account.client_id, test_account.account_id)
    assert a_exists


def test_create_account_exception():
    with pytest.raises(ResourceNotFoundError):
        account_dao.create_account(80, test_account)


def test_get_account_by_id():
    account = account_dao.get_account_by_id(test_client.client_id, test_account.account_id)
    assert test_account.client_id == account.client_id


def test_get_account_by_id_exception():
    with pytest.raises(ResourceNotFoundError):
        account_dao.get_account_by_id(80, 2)


def test_get_all_accounts():
    account1 = Account(0, test_client.client_id, "Savings", 5000)
    account2 = Account(0, test_client.client_id, "Checking", 100)

    account_dao.create_account(test_client.client_id, account1)
    account_dao.create_account(test_client.client_id, account2)

    accounts = account_dao.get_all_accounts(test_client.client_id)

    assert len(accounts) > 2


def test_get_all_accounts_exception():
    with pytest.raises(ResourceNotFoundError):
        account_dao.get_all_accounts(80)


def test_update_account():
    test_account.balance = 3000
    account = account_dao.update_account(test_client.client_id, test_account.account_id, test_account)
    assert test_account.balance == account.balance


def test_update_account_exception():
    with pytest.raises(ResourceNotFoundError):
        account_dao.update_account(80, 1, test_account)


def test_delete_account():
    result = account_dao.get_account_by_id(test_client.client_id, test_account.account_id)
    assert result


def test_delete_account_exception():
    with pytest.raises(ResourceNotFoundError):
        account_dao.delete_account(80, 1)
