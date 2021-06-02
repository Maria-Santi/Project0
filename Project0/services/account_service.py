from abc import ABC, abstractmethod
from typing import List

from entities.account import Account


class AccountService(ABC):

    @abstractmethod
    def add_account(self, client_id: int, account: Account):
        pass

    @abstractmethod
    def retrieve_all_accounts(self, client_id: int):
        pass

    @abstractmethod
    def retrieve_account_by_id(self, client_id: int, account_id: int):
        pass

    @abstractmethod
    def update_account(self, client_id: int, account_id: int, account: Account):
        pass

    @abstractmethod
    def remove_account(self, client_id: int, account_id: int):
        pass

    @abstractmethod
    def retrieve_all_accounts_range(self, client_id: int, to_range: int, from_range: int) -> List[Account]:
        pass

    @abstractmethod
    def get_account_status(self, client_id: int, account_id: int):
        pass

    @abstractmethod
    def transfer_account(self, client_id: int, account_id: int, acc_id: int, transfer_amount: int):
        pass

    @abstractmethod
    def deposit_to_account(self, client_id: int, account_id: int, deposit_amount: int):
        pass

    @abstractmethod
    def withdraw_from_account(self, client_id: int, account_id: int, withdraw_amount: int):
        pass
