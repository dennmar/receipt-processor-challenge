from datetime import date, datetime
from pytest_mock import MockerFixture
from unittest.mock import Mock

from app.purchased_item import PurchasedItem
from app.receipt import Receipt

## Create a mocked receipt with the given attributes.
##
## Parameters:
##     mocker (MockerFixture): fixture used to mock objects and functions
##     name (str): the name of the retailer for the receipt
##     date (date): the purchase date of the receipt
##     time (datetime): the purchase time of the receipt
##     total (float): the total cost in dollars for the receipt
##     items (list[PurchasedItem]): the items purchased on the receipt
##
## Returns:
##     A mocked Receipt with the given attributes.
##
def mock_receipt(mocker: MockerFixture, name: str, date: date, time: datetime,
                 total: float, items: list[PurchasedItem]) -> Receipt:
    receipt = Mock(Receipt)

    receipt.retailer = name
    receipt.purchase_date = date
    receipt.purchase_time = time
    receipt.total_cost = total
    receipt.purchased_items = items

    mocker.patch.object(receipt, 'get_retailer',
                        return_value=receipt.retailer)
    mocker.patch.object(receipt, 'get_purchase_date',
                        return_value=receipt.purchase_date)
    mocker.patch.object(receipt, 'get_purchase_time',
                        return_value=receipt.purchase_time)
    mocker.patch.object(receipt, 'get_total_cost',
                        return_value=receipt.total_cost)
    mocker.patch.object(receipt, 'get_purchased_items',
                        return_value=receipt.purchased_items)

    return receipt

## Create a mocked purchased item with the given attributes.
##
## Parameters:
##     mocker (MockerFixture): fixture used to mock objects and functions
##     desc (str): the short description for the purchased item
##     price (float): the price of the purchased item
##
## Returns:
##     A mocked PurchasedItem with the given attributes.
##
def mock_purchased_item(mocker: MockerFixture, desc: str,
                        price: float) -> PurchasedItem:
    item = Mock(PurchasedItem)
    item.short_description = desc
    item.price = price

    mocker.patch.object(item, 'get_short_description',
                        return_value=item.short_description)
    mocker.patch.object(item, 'get_price', return_value=item.price)

    return item