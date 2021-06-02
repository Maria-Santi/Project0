from flask import Flask, request, jsonify

from daos.account_dao_postgress import AccountDAOPostgres
from entities.account import Account
from exceptions.insufficient_funds_exception import InsufficientFundsError
from exceptions.not_found_exception import ResourceNotFoundError
from services.account_service_impl import AccountServiceImpl

account_dao = AccountDAOPostgres()
account_service = AccountServiceImpl(account_dao)


def create_routes(app: Flask):
    @app.route("/clients/<client_id>/accounts", methods=["POST"])
    def create_account(client_id: str):
        try:
            body = request.json
            account = Account(body["accountID"], int(client_id), body["category"], body["balance"])
            account_service.add_account(int(client_id), account)
            return f"Created account with id {account.account_id} for client {int(client_id)}", 201
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=["GET"])
    def get_account_by_id(client_id: str, account_id: str):
        try:
            account = account_service.retrieve_account_by_id(int(client_id), int(account_id))
            return jsonify(account.as_json_dict()), 200
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/clients/<client_id>/accounts", methods=["GET"])
    def get_all_accounts(client_id: str):
        try:
            to_range = request.args.get("amountLessThan")
            from_range = request.args.get("amountGreaterThan")
            accounts = []
            if to_range is not None:
                if from_range is not None:
                    accounts += account_service.retrieve_all_accounts_range(int(client_id), int(to_range),
                                                                            int(from_range))
            else:
                accounts += account_service.retrieve_all_accounts(int(client_id))
            json_accounts = [a.as_json_dict() for a in accounts]
            return jsonify(json_accounts), 200
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=["PUT"])
    def update_account(client_id: str, account_id: str):
        try:
            body = request.json
            account = Account(body["accountID"], body["clientID"], body["category"], body["balance"])
            account.account_id = int(account_id)
            account_service.update_account(int(client_id), int(account_id), account)
            return f"Account {int(account_id)} for Client {int(client_id)} was updated successfully", 200
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=["DELETE"])
    def delete_account(client_id: str, account_id: str):
        try:
            account_service.remove_account(int(client_id), int(account_id))
            return f"Account {int(account_id)} for Client {int(client_id)} was deleted successfully", 200
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/clients/<client_id>/accounts/<account_id>", methods=["PATCH"])
    def deposits_or_withdraws_account(client_id: str, account_id: str):
        try:
            body = request.json
            if "deposit" in body:
                deposit = body["deposit"]
                account_service.deposit_to_account(int(client_id), int(account_id), int(deposit))
                return f"Deposit to account {account_id} for client {client_id} was completed successfully", 200
            elif "withdraw" in body:
                withdraw = body["withdraw"]
                account_service.withdraw_from_account(int(client_id), int(account_id), int(withdraw))
                return f"Withdrawal from account {account_id} for client {client_id} was completed successfully", 200
        except ResourceNotFoundError as e:
            return str(e), 404
        except InsufficientFundsError as e:
            return str(e), 422

    @app.route("/clients/<client_id>/accounts/<account_id>/transfer/<acc_id>", methods=["PATCH"])
    def transfers_between_account(client_id: str, account_id: str, acc_id: str):
        try:
            body = request.json
            transfer = body["amount"]
            account_service.transfer_account(int(client_id), int(account_id), int(acc_id), int(transfer))
            return f"Transfer from account {account_id} to account {acc_id} " \
                   f"for client {client_id} was completed successfully", 200
        except ResourceNotFoundError as e:
            return str(e), 404
        except InsufficientFundsError as e:
            return str(e), 422
