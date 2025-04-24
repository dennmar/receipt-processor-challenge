from datetime import date, datetime
import math

from app.receipt import Receipt
from app.purchased_item import PurchasedItem

## Calculate the amount of points for the receipt.
##
## Parameters:
##     receipt (Receipt): the receipt to score
##
## Returns:
##     An int for the amount of points scored for the receipt.
##
def score_receipt(receipt: Receipt) -> int:
    total_points = 0

    total_points += _score_name(receipt.get_retailer())
    total_points += _score_purchase_date(receipt.get_purchase_date())
    total_points += _score_purchase_time(receipt.get_purchase_time())
    total_points += _score_total_cost(receipt.get_total_cost())
    total_points += _score_purchased_items(receipt.get_purchased_items())

    return total_points

## Calculate the amount of points for the retailer name of the receipt.
##
## Parameters:
##     name (str): the retailer name of the receipt
##
## Returns:
##     An int for the amount of points scored for the name.
##
def _score_name(name: str) -> int:
    name_points = 0

    for char in name:
        if char.isalnum():
            name_points += 1

    return name_points

## Calculate the amount of points for the purchase date of the receipt.
##
## Parameters:
##     purchase_date (date): the purchase date of the receipt
##
## Returns:
##     An int for the amount of points scored for the purchase date.
##
def _score_purchase_date(purchase_date: date) -> int:
    if purchase_date.day % 2 == 1:
        return 6
    else:
        return 0

## Calculate the amount of points for the purchase time of the receipt.
##
## Parameters:
##     purchase_time (datetime): the purchase time of the receipt
##
## Returns:
##     An int for the amount of points scored for the purchase time.
##
def _score_purchase_time(purchase_time: datetime) -> int:
    at_2_pm = purchase_time.hour == 14 and purchase_time.minute == 0
    after_2_pm = purchase_time.hour >= 14 and not at_2_pm
    before_4_pm = purchase_time.hour < 16

    if after_2_pm and before_4_pm:
        return 10
    else:
        return 0

## Calculate the amount of points for the total cost of the receipt.
##
## Parameters:
##     total_cost (float): the total cost of the receipt
##
## Returns:
##     An int for the amount of points scored for the total cost.
##
def _score_total_cost(total_cost: float) -> int:
    cost_points = 0
    cost_cents, _cost_dollars = math.modf(total_cost)
    cost_cents *= 100

    if cost_cents % 25 == 0:
        cost_points += 25
    if cost_cents == 0:
        cost_points += 50

    return cost_points

## Calculate the amount of points for the purchased items on the receipt.
##
## Parameters:
##     items (list[PurchasedItem]): the items purchased on the receipt
##
## Returns:
##     An int for the amount of points scored for the purchased items.
##
def _score_purchased_items(items: list[PurchasedItem]) -> int:
    item_points = 0

    item_pairs = len(items) // 2
    item_points += 5 * item_pairs

    for item in items:
        short_desc = item.get_short_description()
        if len(short_desc.strip()) % 3 == 0:
            item_points += math.ceil(item.get_price() * 0.2)

    return item_points