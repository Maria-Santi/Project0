from typing import List

from daos.account_dao import AccountDAO
from daos.client_dao_local import ClientDAOLocal
from entities.account import Account
from exceptions.not_found_exception import ResourceNotFoundError


class AccountDAOLocal(AccountDAO):
    account_id_maker = 0
    accounts_table = {}

    def create_account(self, client_id: int, account: Account) -> Account:
        try:
            if client_id in ClientDAOLocal.client_table.keys():
                AccountDAOLocal.account_id_maker += 1
                account.account_id = AccountDAOLocal.account_id_maker
                AccountDAOLocal.accounts_table[AccountDAOLocal.account_id_maker] = {client_id: account}
                return account
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def get_account_by_id(self, client_id: int, account_id: int):
        try:
            if client_id in ClientDAOLocal.client_table.keys():
                try:
                    account = AccountDAOLocal.accounts_table[account_id][client_id]
                    return account
                except KeyError:
                    raise ResourceNotFoundError(f"Account {account_id} for Client {client_id} could not be found")
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def get_all_accounts(self, client_id: int) -> List[Account]:
        try:
            if client_id in ClientDAOLocal.client_table.keys():
                account_list = []
                for a, k in AccountDAOLocal.accounts_table.items():
                    for c in k.keys():
                        if c == client_id:
                            account_list.append(AccountDAOLocal.accounts_table[a][c])
                return account_list
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def update_account(self, client_id: int, account_id: int, account: Account) -> Account:
        try:
            if client_id in ClientDAOLocal.client_table.keys():
                if account_id in AccountDAOLocal.accounts_table.keys():
                    AccountDAOLocal.accounts_table[account_id] = {client_id: account}
                    return account
                else:
                    raise ResourceNotFoundError(f"Account {account.account_id} for Client {client_id} could not be found")
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def delete_account(self, client_id: int, account_id: int) -> bool:
        try:
            if client_id in ClientDAOLocal.client_table.keys():
                try:
                    del AccountDAOLocal.accounts_table[account_id][client_id]
                    return True
                except KeyError:
                    raise ResourceNotFoundError(f"Account {account_id} for Client {client_id} could not be found")
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")
