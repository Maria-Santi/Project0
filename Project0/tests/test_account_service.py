from unittest.mock import MagicMock

import pytest

from daos.account_dao_postgress import AccountDAOPostgres
from entities.account import Account
from exceptions.insufficient_funds_exception import InsufficientFundsError
from exceptions.not_found_exception import ResourceNotFoundError
from services.account_service import AccountService
from services.account_service_impl import AccountServiceImpl

accounts = [Account(1, 1, "Savings", 5000),
            Account(2, 1, "Checking", 300),
            Account(3, 2, "Savings", 10000),
            Account(4, 2, "Checking", 500),
            Account(5, 3, "Savings", 7000),
            Account(6, 3, "Checking", 1000),
            Account(7, 3, "Savings", 3000),
            Account(8, 3, "Savings", 2000)]

mock_dao = AccountDAOPostgres()
mock_dao.get_all_accounts = MagicMock(return_value=accounts)
mock_dao.update_account = MagicMock(return_values=accounts)
mock_dao.get_account_belongs_to_client = MagicMock(return_values=accounts)
mock_dao.get_client_exists = MagicMock(return_values=accounts)
accounts = mock_dao.get_all_accounts()

account_service: AccountService = AccountServiceImpl(mock_dao)


def test_get_account_status():
    result = account_service.get_account_status(1, 1)
    assert result


def test_get_all_accounts_range():
    result = account_service.retrieve_all_accounts_range(3, 7000, 1000)
    assert len(result) >= 2


def test_transfer_account():
    balance = account_service.transfer_account(2, 3, 4, 2000)
    assert balance[1] == 2500 and balance[0] == 8000


def test_transfer_account_exception_1():
    with pytest.raises(ResourceNotFoundError):
        account_service.transfer_account(80, 100, 700, 500)


def test_transfer_account_exception_2():
    with pytest.raises(InsufficientFundsError):
        account_service.transfer_account(3, 6, 7, 3000)


def test_deposit_to_account():
    balance = account_service.deposit_to_account(1, 1, 1000)
    assert balance == 6000


def test_deposit_to_account_exception():
    with pytest.raises(ResourceNotFoundError):
        account_service.deposit_to_account(80, 700, 500)


def test_withdraw_from_account():
    balance = account_service.withdraw_from_account(3, 5, 1000)
    assert balance == 6000


def test_withdraw_from_account_exception_1():
    with pytest.raises(ResourceNotFoundError):
        account_service.withdraw_from_account(80, 700, 500)


def test_withdraw_from_account_exception_2():
    with pytest.raises(InsufficientFundsError):
        account_service.withdraw_from_account(1, 2, 1000)
