from flask import Flask

## Create the Flask application for the receipt processor.
##
## Returns:
##     A Flask object representing the receipt processor application.
##
def create_app() -> Flask:
    app = Flask(__name__)

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