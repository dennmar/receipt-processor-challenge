from flask import Flask, request

from app.receipt_database import ReceiptDatabase
from app.point_calculator import score_receipt

## Create the Flask application for the receipt processor.
##
## Returns:
##     A Flask object representing the receipt processor application.
##
def create_app() -> Flask:
    app = Flask(__name__)
    receipt_db = ReceiptDatabase()

    ## Store the receipt data as a receipt in the database.
    ##
    ## Returns:
    ##     On success, a tuple is returned which contains a dict specifying
    ##     the unique id of the receipt and an int for the response code.
    ##     On failure, a tuple is returned which contains a string for the
    ##     cause of failure and an int for the response code.
    ##
    @app.route("/receipts/process", methods=['POST'])
    def store_receipt() -> tuple:
        try:
            receipt_data = request.get_json()
            receipt_id = receipt_db.add_receipt(receipt_data)
            return {'id': receipt_id}, 200
        except (ValueError, KeyError) as err:
            return str(err.args[0]), 400
        except Exception as err:
            return repr(err), 500

    ## Retrieve the amount of points for the receipt with the given id.
    ##
    ## Parameters:
    ##     id (str): the id of the receipt
    ##
    ## Returns:
    ##     On success, a tuple is returned which contains a dict specifying
    ##     the amount of points calculated for the receipt with the matching
    ##     id and an int for the response code. On failure, a tuple is
    ##     returned which contains a string describing the cause of failure
    ##     and an int for the response code.
    ##
    @app.route("/receipts/<id>/points")
    def get_points(id) -> tuple:
        try:
            receipt = receipt_db.get_receipt(id)

            if receipt is not None:
                points = score_receipt(receipt)
                return {'points': points}, 200
            else:
                return f'No receipt found with the id of {id}', 404
        except Exception as err:
            return repr(err), 500

    return app