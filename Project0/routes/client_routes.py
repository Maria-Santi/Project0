from flask import Flask, request, jsonify

from daos.client_dao_postgres import ClientDAOPostgres
from entities.client import Client
from exceptions.not_found_exception import ResourceNotFoundError
from services.client_service_impl import ClientServiceImpl

client_dao = ClientDAOPostgres()
client_service = ClientServiceImpl(client_dao)


def create_routes(app: Flask):
    @app.route("/clients", methods=["POST"])
    def create_client():
        body = request.json
        client = Client(body["clientID"], body["clientName"])
        client_service.add_client(client)
        return f"Client {client.client_id} created", 201

    @app.route("/clients/<client_id>", methods=["GET"])
    def get_client_by_id(client_id: str):
        try:
            client = client_service.retrieve_client_by_id(int(client_id))
            return jsonify(client.as_json_dict()), 200
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/clients", methods=["GET"])
    def get_all_clients():
        clients = client_service.retrieve_all_clients()
        json_clients = [c.as_json_dict() for c in clients]
        return jsonify(json_clients)

    @app.route("/clients/<client_id>", methods=["PUT"])
    def update_client(client_id: str):
        try:
            body = request.json
            client = Client(body["clientID"], body["clientName"])
            client.client_id = int(client_id)
            client_service.update_client(int(client_id), client)
            return f"Client {client.client_id} updated successfully", 200
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/clients/<client_id>", methods=["DELETE"])
    def delete_client(client_id: str):
        try:
            client_service.remove_client(int(client_id))
            return f"Client {client_id} was deleted successfully", 205
        except ResourceNotFoundError as e:
            return str(e), 404
