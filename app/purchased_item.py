## An item purchased from a retailer.
##
class PurchasedItem:
    ## Initialize member variables for the purchased item.
    ##
    ## Parameters:
    ##     item (dict): a dict with keys "shortDescription" and "price" for
    ##                  the purchased item
    ##
    def __init__(self, item: dict):
        self.short_description = item['shortDescription']
        self.price = self._parse_price(item['price'])

    ## Parse the price from the given string.
    ##
    ## Parameters:
    ##     price_str (str): the string to parse for the price
    ##
    ## Returns:
    ##     A float for the parsed price.
    ##
    def _parse_price(self, price_str: str) -> float:
        return float(price_str)

    ## Retrieve the short description for the purchased item.
    ##
    ## Returns:
    ##     A string for the short description.
    ##
    def get_short_description(self) -> str:
        return self.short_description

    ## Retrieve the price for the purchased item.
    ##
    ## Returns:
    ##     A float for the price.
    ##
    def get_price(self) -> float:
        return self.price