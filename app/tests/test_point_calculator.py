import math
from datetime import date, datetime
from pytest_mock import MockerFixture

import app.point_calculator as pc
from app.purchased_item import PurchasedItem
from app.tests.helpers.mockers import mock_purchased_item, mock_receipt

class TestScoreName:
    def test_empty_string(self) -> None:
        assert pc._score_name('') == 0

    def test_normal_name(self) -> None:
        assert pc._score_name('Target') == 6

    def test_numbers(self) -> None:
        assert pc._score_name('0987654321') == 10

    def test_name_with_numbers(self) -> None:
        assert pc._score_name('Store123') == 8

    def test_non_alphanumeric(self) -> None:
        assert pc._score_name('!@#$%^& *()-=./') == 0

    def test_name_with_non_alphanumeric(self) -> None:
        assert pc._score_name('Warehouse [A-B/C]') == 12

    def test_mixed(self) -> None:
        assert pc._score_name('M&M Corner Market #2') == 15

class TestScorePurchaseDate:
    def test_odd_day(self) -> None:
        assert pc._score_purchase_date(date(2000, 2, 1)) == 6

    def test_even_day(self) -> None:
        assert pc._score_purchase_date(date(2011, 3, 22)) == 0

class TestScorePurchaseTime:
    def test_before_2_pm(self) -> None:
        before_2_pm = datetime(2020, 5, 1, hour=1, minute=1)
        assert pc._score_purchase_time(before_2_pm) == 0

    def test_at_2_pm(self) -> None:
        at_2_pm = datetime(2021, 10, 2, hour=14, minute=0)
        assert pc._score_purchase_time(at_2_pm) == 0

    def test_at_201_pm(self) -> None:
        at_201_pm = datetime(1900, 2, 3, hour=14, minute=1)
        assert pc._score_purchase_time(at_201_pm) == 10

    def test_at_323_pm(self) -> None:
        at_323_pm = datetime(1980, 12, 30, hour=15, minute=23)
        assert pc._score_purchase_time(at_323_pm) == 10

    def test_at_359_pm(self) -> None:
        at_359_pm = datetime(1967, 8, 19, hour=15, minute=59)
        assert pc._score_purchase_time(at_359_pm) == 10

    def test_at_4_pm(self) -> None:
        at_4_pm = datetime(1950, 9, 5, hour=16, minute=0)
        assert pc._score_purchase_time(at_4_pm) == 0

    def test_after_4_pm(self) -> None:
        after_4_pm = datetime(1899, 1, 2, hour=18, minute=34)
        assert pc._score_purchase_time(after_4_pm) == 0

class TestScoreTotalCost:
    def test_zero(self) -> None:
        assert pc._score_total_cost(0) == 75

    def test_1_cent(self) -> None:
        assert pc._score_total_cost(75.1) == 0

    def test_24_cents(self) -> None:
        assert pc._score_total_cost(100.24) == 0

    def test_25_cents(self) -> None:
        assert pc._score_total_cost(5.25) == 25

    def test_26_cents(self) -> None:
        assert pc._score_total_cost(78.26) == 0

    def test_49_cents(self) -> None:
        assert pc._score_total_cost(2.49) == 0

    def test_50_cents(self) -> None:
        assert pc._score_total_cost(8.50) == 25

    def test_51_cents(self) -> None:
        assert pc._score_total_cost(20.51) == 0

    def test_74_cents(self) -> None:
        assert pc._score_total_cost(54.71) == 0

    def test_75_cents(self) -> None:
        assert pc._score_total_cost(0.75) == 25

    def test_76_cents(self) -> None:
        assert pc._score_total_cost(5420.76) == 0

    def test_99_cents(self) -> None:
        assert pc._score_total_cost(90.99) == 0

    def test_round_dollar_amt(self) -> None:
        assert pc._score_total_cost(17.00) == 75

class TestScorePurchasedItems:
    PRICE_FACTOR = 0.2

    def test_no_items(self) -> None:
        assert pc._score_purchased_items([]) == 0

    def test_empty_desc(self, mocker: MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, '', 2.50)
        expected_score = int(math.ceil(mock_item.price * self.PRICE_FACTOR))
        assert pc._score_purchased_items([mock_item]) == expected_score

    def test_non_mult3_desc(self, mocker: MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, 'Hi', 1.0)
        assert pc._score_purchased_items([mock_item]) == 0

    def test_mult3_desc(self, mocker: MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, 'And', 523)
        expected_score = int(math.ceil(mock_item.price * self.PRICE_FACTOR))
        assert pc._score_purchased_items([mock_item]) == expected_score

    def test_mult3_starting_whitespace(self, mocker: MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, '  Course', 10.40)
        expected_score = int(math.ceil(mock_item.price * self.PRICE_FACTOR))
        assert pc._score_purchased_items([mock_item]) == expected_score

    def test_non_mult3_starting_whitespace(self, mocker: MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, '     Food', 10.40)
        assert pc._score_purchased_items([mock_item]) == 0

    def test_mult3_ending_whitespace(self, mocker: MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, 'Ice Cream    ', 934.32)
        expected_score = int(math.ceil(mock_item.price * self.PRICE_FACTOR))
        assert pc._score_purchased_items([mock_item]) == expected_score

    def test_non_mult3_ending_whitespace(self, mocker: MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, 'Tarantulas ', 10.40)
        assert pc._score_purchased_items([mock_item]) == 0

    def test_mult3_whitespace_both(self, mocker:MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, '   Modern Computer ', 4100.89)
        expected_score = int(math.ceil(mock_item.price * self.PRICE_FACTOR))
        assert pc._score_purchased_items([mock_item]) == expected_score

    def test_non_mult3_whitespace_both(self, mocker:MockerFixture) -> None:
        mock_item = mock_purchased_item(mocker, ' Rock ', 100204.48)
        assert pc._score_purchased_items([mock_item]) == 0

    def test_two_items(self, mocker: MockerFixture) -> None:
        mock_item1 = mock_purchased_item(mocker, '4', 23.19)
        mock_item2 = mock_purchased_item(mocker, 'Igloo', 5.20)
        assert pc._score_purchased_items([mock_item1, mock_item2]) == 5

    def test_multiple_items_odd(self, mocker: MockerFixture) -> None:
        prices = [90.20, 143.21, 0.50, 10.34, 40.87]
        items = [
            mock_purchased_item(mocker, 'Parkas', prices[0]),
            mock_purchased_item(mocker, 'Shovels', prices[1]),
            mock_purchased_item(mocker, 'Snowballs', prices[2]),
            mock_purchased_item(mocker, 'Ice', prices[3]),
            mock_purchased_item(mocker, 'Heavy Boots', prices[4])
        ]

        expected_score = 10
        expected_score += int(math.ceil(prices[0] * self.PRICE_FACTOR))
        expected_score += int(math.ceil(prices[2] * self.PRICE_FACTOR))
        expected_score += int(math.ceil(prices[3] * self.PRICE_FACTOR))

        assert pc._score_purchased_items(items) == expected_score

    def test_multiple_items_even(self, mocker: MockerFixture) -> None:
        prices = [102.40, 345.12, 534.95, 5.69, 46.32, 458.11]
        items = [
            mock_purchased_item(mocker, 'Helicopter', prices[0]),
            mock_purchased_item(mocker, 'Tank', prices[1]),
            mock_purchased_item(mocker, 'Scooter', prices[2]),
            mock_purchased_item(mocker, 'Volkswagen', prices[3]),
            mock_purchased_item(mocker, 'Unicycle', prices[4]),
            mock_purchased_item(mocker, 'Batmobile', prices[5])
        ]

        expected_score = 15
        expected_score += int(math.ceil(prices[5] * self.PRICE_FACTOR))

        assert pc._score_purchased_items(items) == expected_score

class TestScoreReceipt:
    def test_example1(self, mocker: MockerFixture) -> None:
        receipt = mock_receipt(
            mocker,
            'Target',
            date(2022, 1, 1),
            datetime(2022, 1, 1, hour=13, minute=1),
            35.35,
            [
                mock_purchased_item(mocker, 'Mountain Dew 12PK', 6.49),
                mock_purchased_item(mocker, 'Emils Cheese Pizza', 12.25),
                mock_purchased_item(mocker, 'Knorr Creamy Chicken', 1.26),
                mock_purchased_item(mocker, 'Doritos Nacho Cheese', 3.35),
                mock_purchased_item(mocker, '   Klarbrunn 12-PK 12 FL OZ  ', 12.00)
            ]
        )

        assert pc.score_receipt(receipt) == 28

    def test_example2(self, mocker: MockerFixture) -> None:
        receipt = mock_receipt(
            mocker,
            'M&M Corner Market',
            date(2022, 3, 20),
            datetime(2022, 3, 20, hour=14, minute=33),
            9.00,
            [
                mock_purchased_item(mocker, 'Gatorade', 2.25),
                mock_purchased_item(mocker, 'Gatorade', 2.25),
                mock_purchased_item(mocker, 'Gatorade', 2.25),
                mock_purchased_item(mocker, 'Gatorade', 2.25)
            ]
        )

        assert pc.score_receipt(receipt) == 109

    def test_example3(self, mocker: MockerFixture) -> None:
        receipt = mock_receipt(
            mocker,
            'Jim Jr. and Rhino\'s Frozen Grill & Hot Lemonade v3.0',
            date(2025, 12, 31),
            datetime(2025, 12, 31, hour=16, minute=0),
            52.75,
            [
                mock_purchased_item(mocker, 'Lemonade Extra Hot ', 52.75)
            ]
        )

        assert pc.score_receipt(receipt) == 81