from typing import List

from daos.account_dao import AccountDAO
from entities.account import Account
from exceptions.not_found_exception import ResourceNotFoundError
from utils.connection_util import connection


class AccountDAOPostgres(AccountDAO):

    # every account method has to check if a client exists
    def get_client_exists(self, client_id: int):
        c_sql = """select * from client where client_id = %s"""
        c_cursor = connection.cursor()
        c_cursor.execute(c_sql, [client_id])
        client_exists = c_cursor.fetchone()
        return client_exists

    # Account methods would check if client exists and if account exists, but not if account belonged to the client,
    # so requests would be successful if both existed. This method solves that
    def get_account_belongs_to_client(self, client_id: int, account_id: int):
        sql = """select * from account where client_id = %s and account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (client_id, account_id))
        a_exists = cursor.fetchone()
        return a_exists

    def create_account(self, client_id: int, account: Account) -> Account:
        try:
            client_exists = self.get_client_exists(client_id)
            if client_exists is not None:
                sql = """insert into account (client_id, category, balance) values (%s, %s, %s) returning account_id"""
                cursor = connection.cursor()
                cursor.execute(sql, (client_id, account.category, account.balance))
                connection.commit()
                a_id = cursor.fetchone()[0]
                account.account_id = a_id
                return account
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def get_account_by_id(self, client_id: int, account_id: int):
        try:
            client_exists = self.get_client_exists(client_id)
            if client_exists is not None:
                sql = """select * from account where client_id = %s and account_id = %s"""
                cursor = connection.cursor()
                cursor.execute(sql, (client_id, account_id))
                record = cursor.fetchone()
                if record is not None:
                    account = Account(*record)
                    return account
                else:
                    raise ResourceNotFoundError(f"Account {account_id} for Client {client_id} could not be found")
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def get_all_accounts(self, client_id: int) -> List[Account]:
        try:
            client_exists = self.get_client_exists(client_id)
            if client_exists is not None:
                sql = """select * from account where client_id = %s"""
                cursor = connection.cursor()
                cursor.execute(sql, [client_id])
                records = cursor.fetchall()
                if not records:
                    raise ResourceNotFoundError(f"Client {client_id} has no accounts")
                if records is not None:
                    accounts = [Account(*record) for record in records]
                    return accounts
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def update_account(self, client_id: int, account_id: int, account: Account) -> Account:
        try:
            client_exists = self.get_client_exists(client_id)
            if client_exists is not None:
                sql = """update account set category = %s, balance = %s where account_id = %s and client_id = %s
                        returning account_id"""
                cursor = connection.cursor()
                cursor.execute(sql, (account.category, account.balance, account_id, client_id))
                connection.commit()
                a_id = cursor.fetchone()
                if a_id is not None:
                    return account
                else:
                    raise ResourceNotFoundError(f"Account {account_id} for Client {client_id} could not be found")
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def delete_account(self, client_id: int, account_id: int) -> bool:
        try:
            client_exists = self.get_client_exists(client_id)
            if client_exists is not None:
                sql = """delete from account where account_id = %s and client_id = %s returning account_id"""
                cursor = connection.cursor()
                cursor.execute(sql, (account_id, client_id))
                connection.commit()
                a_id = cursor.fetchone()
                if a_id is not None:
                    return True
                else:
                    raise ResourceNotFoundError(f"Account {account_id} for Client {client_id} could not be found")
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")
