from typing import List

from daos.client_dao import ClientDAO
from entities.client import Client
from exceptions.not_found_exception import ResourceNotFoundError
from utils.connection_util import connection


class ClientDAOPostgres(ClientDAO):

    def create_client(self, client: Client) -> Client:
        sql = """insert into client (client_name) values (%s) returning client_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [client.client_name])
        connection.commit()
        c_id = cursor.fetchone()[0]
        client.client_id = c_id
        return client

    def get_client_by_id(self, client_id: int) -> Client:
        try:
            sql = """select * from client where client_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, [client_id])
            record = cursor.fetchone()
            if record is not None:
                client = Client(*record)
                return client
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    def get_all_clients(self) -> List[Client]:
        sql = """select * from client"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        clients = [Client(*record) for record in records]
        return clients

    def update_client(self, client_id: int, client: Client) -> Client:
        try:
            sql = """update client set client_name = %s where client_id = %s returning client_id"""
            cursor = connection.cursor()
            cursor.execute(sql, (client.client_name, client_id))
            connection.commit()
            c_id = cursor.fetchone()
            if c_id is not None:
                return client
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")

    # also deletes accounts if client has any because of referential integrity
    def delete_client(self, client_id: int) -> bool:
        try:
            a_sql = "delete from account where client_id = %s"
            a_cursor = connection.cursor()
            a_cursor.execute(a_sql, [client_id])
            connection.commit()
            sql = """delete from client where client_id = %s returning client_id"""
            cursor = connection.cursor()
            cursor.execute(sql, [client_id])
            connection.commit()
            c_id = cursor.fetchone()
            if c_id is not None:
                return True
            else:
                raise KeyError
        except KeyError:
            raise ResourceNotFoundError(f"Client {client_id} could not be found")
