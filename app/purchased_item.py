import pprint

## An item purchased from a retailer.
##
class PurchasedItem:
    ## Initialize member variables for the purchased item.
    ##
    ## Parameters:
    ##     item (dict): a dict with keys "shortDescription" and "price" for
    ##                  the purchased item
    ##
    ## Raises:
    ##     KeyError: if item doesn't contain "shortDescription" or "price"
    ##               as keys
    ##
    def __init__(self, item: dict):
        expected_keys = ['shortDescription', 'price']

        for key in expected_keys:
            if not key in item:
                error_msg = f'Item in receipt must define the {key} key:\n'
                item_str = pprint.pformat(item, sort_dicts=False)
                raise KeyError(error_msg + item_str)

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