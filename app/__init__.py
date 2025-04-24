from flask import Flask, request

from app.receipt_database import ReceiptDatabase

receipt_db = ReceiptDatabase()

## Create the Flask application for the receipt processor.
##
## Returns:
##     A Flask object representing the receipt processor application.
##
def create_app() -> Flask:
    app = Flask(__name__)

    ## Store the receipt data as a receipt in the database.
    ##
    ## Returns:
    ##     A dict with the key "id" for the unique id of the receipt stored in
    ##     the database.
    ##
    @app.route("/receipts/process", methods=['POST'])
    def store_receipt() -> dict:
        receipt_data = request.get_json()
        receipt_id = receipt_db.add_receipt(receipt_data)
        return {'id': receipt_id}

    ## Retrieve the amount of points for the receipt with the given id.
    ##
    ## Parameters:
    ##     id (str): the id of the receipt
    ##
    ## Returns:
    ##     A dict with the key "points" that specifies the amount of points
    ##     calculated for the receipt with the matching id.
    @app.route("/receipts/<id>/points")
    def get_points(id) -> dict:
        return {'points': 0}

    return app