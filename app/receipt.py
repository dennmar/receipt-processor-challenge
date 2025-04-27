from datetime import date, datetime
import pprint

from app.purchased_item import PurchasedItem

## A receipt for items purchased from a retailer.
##
class Receipt:
    ## Initialize member variables for the receipt.
    ##
    ## Parameters:
    ##     receipt_data (dict): a dict with keys "retailer", "purchaseDate",
    ##                          "purchaseTime", "total", and "items" for the
    ##                          receipt
    ##
    ## Raises:
    ##     KeyError: if receipt_data doesn't contain "retailer", "purchaseDate",
    ##               "purchaseTime", "total", or "items" as keys
    ##
    def __init__(self, receipt_data: dict):
        expected_keys = [
            'retailer', 'purchaseDate', 'purchaseTime', 'total', 'items'
        ]

        for key in expected_keys:
            if not key in receipt_data:
                error_msg = f'Receipt must define the {key} key:\n'
                receipt_str = pprint.pformat(receipt_data, sort_dicts=False)
                raise KeyError(error_msg + receipt_str)

        self.retailer = receipt_data['retailer']
        self.purchase_date = self._parse_date(receipt_data['purchaseDate'])
        self.purchase_time = self._parse_time(receipt_data['purchaseTime'])
        self.total_cost = self._parse_total_cost(receipt_data['total'])
        self.purchased_items = self._parse_purchased_items(receipt_data['items'])

    ## Parse the purchase date from the given string.
    ##
    ## Parameters:
    ##     purchase_date (str): the string to parse for the receipt date
    ##
    ## Raises:
    ##     ValueError: if the purchase date format doesn't match "YYYY-MM-DD"
    ##
    ## Returns:
    ##     A date for the purchase date of the receipt.
    ##
    def _parse_date(self, purchase_date: str) -> date:
        try:
            return date.fromisoformat(purchase_date)
        except ValueError:
            error_msg = 'Receipt purchase date does not match "YYYY-MM-DD": '
            raise ValueError(error_msg + purchase_date)

    ## Parse the purchase time from the given string.
    ##
    ## Parameters:
    ##     purchase_time (str): the string to parse for the receipt time
    ##
    ## Raises:
    ##     ValueError: if the purchase time format doesn't match "H:M"
    ##
    ## Returns:
    ##     A datetime for the purchase time of the receipt.
    ##
    def _parse_time(self, purchase_time: str) -> datetime:
        try:
            return datetime.strptime(purchase_time, '%H:%M').time()
        except ValueError:
            error_msg = 'Receipt purchase time does not match "H:M": '
            raise ValueError(error_msg + purchase_time)

    ## Parse the total cost from the given string.
    ##
    ## Parameters:
    ##     total_cost (str): the string to parse for the receipt's total cost
    ##
    ## Raises:
    ##     ValueError: if the total cost cannot be parsed from the given string
    ##
    ## Returns:
    ##     A float for the total cost of the receipt.
    ##
    def _parse_total_cost(self, total_cost: str) -> float:
        try:
            return float(total_cost)
        except ValueError:
            error_msg = 'Total could not be parsed for receipt: '
            raise ValueError(error_msg + total_cost)

    ## Parse the purchased items from the given list.
    ##
    ## Parameters:
    ##     items (list[dict]): a list where each element is a dict containing
    ##                         the keys "shortDescription" and "price" for the
    ##                         purchased item
    ##
    ## Returns:
    ##     A list of PurchasedItems representing the receipt's purchased items.
    ##
    def _parse_purchased_items(self, items: list[dict]) -> list[PurchasedItem]:
        return [PurchasedItem(item) for item in items]

    ## Retrieve the retailer for the receipt.
    ##
    ## Returns:
    ##     A string for the name of the retailer.
    ##
    def get_retailer(self) -> str:
        return self.retailer

    ## Retrieve the purchase date for the receipt.
    ##
    ## Returns:
    ##     A date for the purchase date.
    ##
    def get_purchase_date(self) -> date:
        return self.purchase_date

    ## Retrieve the purchase time for the receipt.
    ##
    ## Returns:
    ##     A Time for the purchase time.
    ##
    def get_purchase_time(self) -> datetime:
        return self.purchase_time

    ## Retrieve the total cost for the receipt.
    ##
    ## Returns:
    ##     A float for the total cost in dollars.
    ##
    def get_total_cost(self) -> float:
        return self.total_cost

    ## Retrieve the purchased items for the receipt.
    ##
    ## Returns:
    ##     A list of PurchasedItems for the items purchased on the receipt.
    ##
    def get_purchased_items(self) -> list[PurchasedItem]:
        return self.purchased_items

    ## Check if the given object is equivalent to this object.
    ##
    ## Parameters:
    ##     other (any): the other object to check for equivalence
    ##
    ## Returns:
    ##     True if the given object is equivalent to this object; false
    ##     otherwise.
    ##
    def __eq__(self, other: any) -> bool:
        if isinstance(other, Receipt):
            self_attr = (
                self.retailer,
                self.purchase_date,
                self.purchase_time,
                self.total_cost,
                self.purchased_items
            )
            other_attr = (
                other.retailer,
                other.purchase_date,
                other.purchase_time,
                other.total_cost,
                other.purchased_items
            )
            return self_attr == other_attr

        return False