from app.receipt import Receipt

## A database storing receipt information.
##
class ReceiptDatabase:
    ## Initialize member variables for the database.
    ##
    def __init__(self) -> None:
        self.receipts = {}
        self._receipts_added = 0

    ## Store the receipt in the database.
    ##
    ## Parameters:
    ##     receipt_data (dict): a dict with keys "retailer", "purchaseDate",
    ##                          "purchaseTime", "total", and "items" for the
    ##                          receipt
    ##
    ## Returns:
    ##     A string for the unique id of the receipt.
    ##
    def add_receipt(self, receipt_data: dict) -> str:
        receipt = Receipt(receipt_data)
        id = self._generate_id(receipt)
        self.receipts[id] = receipt
        return id

    ## Retrieve the receipt that matches the given id.
    ##
    ## Parameters:
    ##     id (str): the unique id of the receipt to retrieve
    ##
    ## Returns:
    ##     A Receipt for the receipt that matches the id or None if no receipt
    ##     was found.
    ##
    def get_receipt(self, id: str) -> Receipt:
        if id in self.receipts:
            return self.receipts[id]
        else:
            return None

    ## Generate the unique id for the given receipt.
    ##
    ## Parameters:
    ##     _receipt (Receipt): the receipt to generate the id for
    ##
    ## Returns:
    ##     A string for the unique id of the given receipt.
    ##
    def _generate_id(self, _receipt: Receipt) -> str:
        self._receipts_added += 1
        return str(self._receipts_added)