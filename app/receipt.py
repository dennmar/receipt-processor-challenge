from datetime import date, datetime

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
    def __init__(self, receipt_data: dict):
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
    ## Returns:
    ##     A date for the purchase date of the receipt.
    ##
    def _parse_date(self, purchase_date: str) -> date:
        return date.fromisoformat(purchase_date)

    ## Parse the purchase time from the given string.
    ##
    ## Parameters:
    ##     purchase_time (str): the string to parse for the receipt time
    ##
    ## Returns:
    ##     A datetime for the purchase time of the receipt.
    ##
    def _parse_time(self, purchase_time: str) -> datetime:
        return datetime.strptime(purchase_time, '%H:%M').time()

    ## Parse the total cost from the given string.
    ##
    ## Parameters:
    ##     total_cost (str): the string to parse for the receipt's total cost
    ##
    ## Returns:
    ##     A float for the total cost of the receipt.
    ##
    def _parse_total_cost(self, total_cost: str) -> float:
        return float(total_cost)

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