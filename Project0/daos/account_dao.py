from abc import ABC, abstractmethod
from typing import List

from entities.account import Account


class AccountDAO(ABC):
    @abstractmethod
    def get_client_exists(self, client_id: int):
        pass

    @abstractmethod
    def get_account_belongs_to_client(self, client_id: int, account_id: int) -> bool:
        pass

    @abstractmethod
    def create_account(self, client_id: int, account: Account) -> Account:
        pass

    @abstractmethod
    def get_account_by_id(self, client_id: int, account_id: int):
        pass

    @abstractmethod
    def get_all_accounts(self, client_id: int) -> List[Account]:
        pass

    @abstractmethod
    def update_account(self, client_id: int, account_id: int, account: Account) -> Account:
        pass

    @abstractmethod
    def delete_account(self, client_id: int, account_id: int) -> bool:
        pass
