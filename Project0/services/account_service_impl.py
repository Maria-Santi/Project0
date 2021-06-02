from typing import List

from daos.account_dao import AccountDAO
from entities.account import Account
from exceptions.insufficient_funds_exception import InsufficientFundsError
from exceptions.not_found_exception import ResourceNotFoundError
from services.account_service import AccountService


class AccountServiceImpl(AccountService):

    def __init__(self, account_dao: AccountDAO):
        self.account_dao = account_dao

    def add_account(self, client_id: int, account: Account):
        return self.account_dao.create_account(client_id, account)

    def retrieve_all_accounts(self, client_id: int):
        return self.account_dao.get_all_accounts(client_id)

    def retrieve_account_by_id(self, client_id: int, account_id: int):
        return self.account_dao.get_account_by_id(client_id, account_id)

    def update_account(self, client_id: int, account_id: int, account: Account):
        return self.account_dao.update_account(client_id, account_id, account)

    def remove_account(self, client_id: int, account_id: int):
        return self.account_dao.delete_account(client_id, account_id)

    # created this method so that the following methods would be able to raise an exception
    # if client or account does not exist. This is for the account_service tests
    # The exception tests would not pass unless the exceptions were raised in this file.
    # I am assuming it is because of Mock test?
    # Exceptions would work in Postman without having to raise the exceptions in this file.
    def get_account_status(self, client_id: int, account_id: int):
        status = False
        accounts = self.account_dao.get_all_accounts(client_id)
        for acc in accounts:
            if acc.account_id == account_id:
                status = self.account_dao.get_account_belongs_to_client(client_id, account_id)
        return status

    def retrieve_all_accounts_range(self, client_id: int, to_range: int, from_range: int) -> List[Account]:
        status = self.account_dao.get_client_exists(client_id)
        if not status:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")
        else:
            accounts = self.account_dao.get_all_accounts(client_id)
            ranged_accounts = []
            for acc in accounts:
                if from_range < acc.balance < to_range:
                    ranged_accounts.append(acc)
            return ranged_accounts

    def deposit_to_account(self, client_id: int, account_id: int, deposit: int):
        status = self.get_account_status(client_id, account_id)
        if not status:
            raise ResourceNotFoundError(f"Account {account_id} for Client {client_id} could not be found")
        else:
            accounts = self.account_dao.get_all_accounts(client_id)
            for acc in accounts:
                if account_id == acc.account_id:
                    acc.balance += deposit
                    self.account_dao.update_account(client_id, account_id, acc)
                    return acc.balance

    def withdraw_from_account(self, client_id: int, account_id: int, withdraw: int):
        status = self.get_account_status(client_id, account_id)
        if not status:
            raise ResourceNotFoundError(f"Account {account_id} for Client {client_id} could not be found")
        else:
            accounts = self.account_dao.get_all_accounts(client_id)
            for acc in accounts:
                if account_id == acc.account_id:
                    if acc.balance >= withdraw:
                        acc.balance -= withdraw
                        self.account_dao.update_account(client_id, account_id, acc)
                        return acc.balance
                    else:
                        raise InsufficientFundsError(
                            f"Insufficient funds in account {account_id} for client {client_id}")

    def transfer_account(self, client_id: int, account_id: int, acc_id: int, transfer_amount: int):
        balance = []
        balance1 = self.withdraw_from_account(client_id, account_id, transfer_amount)
        balance2 = self.deposit_to_account(client_id, acc_id, transfer_amount)
        balance.append(balance1)
        balance.append(balance2)
        return balance
