from datetime import date, datetime
from pytest_mock import MockerFixture

from app.receipt_database import ReceiptDatabase
from app.tests.helpers.mockers import mock_purchased_item, mock_receipt

class TestGenerateId:
    def test_first_generate(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt = mock_receipt(
            mocker,
            'Walmart',
            date(2030, 5, 6),
            datetime(2030, 5, 6, hour=6, minute=12),
            12.74,
            [
                mock_purchased_item(mocker, 'Popcorn', 5.99),
                mock_purchased_item(mocker, 'Butter', 6.75)
            ]
        )

        assert receipt_db._generate_id(receipt) == '1'

    def test_consecutive_generates(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt1 = mock_receipt(
            mocker,
            'Walmart',
            date(2030, 5, 6),
            datetime(2030, 5, 6, hour=6, minute=12),
            12.74,
            [
                mock_purchased_item(mocker, 'Popcorn', 5.99),
                mock_purchased_item(mocker, 'Butter', 6.75)
            ]
        )
        receipt2 = mock_receipt(
            mocker,
            'Walgreens',
            date(2030, 5, 7),
            datetime(2030, 5, 7, hour=9, minute=56),
            2.99,
            [
                mock_purchased_item(mocker, 'Chocolate', 2.99)
            ]
        )

        receipt_db._generate_id(receipt1)
        assert receipt_db._generate_id(receipt2) == '2'

    def test_same_receipt_generates(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt = mock_receipt(
            mocker,
            'Fareway',
            date(2014, 1, 15),
            datetime(2014, 1, 15, hour=13, minute=2),
            2.68,
            [
                mock_purchased_item(mocker, 'Apples', 2.68)
            ]
        )

        receipt_db._generate_id(receipt) == '1'
        assert receipt_db._generate_id(receipt) == '2'

    def test_multiple_generates(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt = mock_receipt(
            mocker,
            'Fareway',
            date(2014, 1, 15),
            datetime(2014, 1, 15, hour=13, minute=2),
            2.68,
            [
                mock_purchased_item(mocker, 'Apples', 2.68)
            ]
        )

        ids = []
        for i in range(100):
            ids.append(receipt_db._generate_id(receipt))

        assert ids == [str(i) for i in range(1, 101)]

class TestGetReceipt:
    def test_empty_db(self) -> None:
        receipt_db = ReceiptDatabase()
        assert receipt_db.get_receipt('0') == None

    def test_get_stored(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt = mock_receipt(
            mocker,
            'Hyvee',
            date(2018, 7, 9),
            datetime(2018, 7, 9, hour=16, minute=28),
            0.99,
            [
                mock_purchased_item(mocker, 'Cabbage', 0.99)
            ]
        )

        receipt_db.receipts['27'] = receipt
        assert receipt_db.get_receipt('27') == receipt

    def test_missing(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt = mock_receipt(
            mocker,
            'Hyvee',
            date(2018, 7, 9),
            datetime(2018, 7, 9, hour=16, minute=28),
            0.99,
            [
                mock_purchased_item(mocker, 'Cabbage', 0.99)
            ]
        )

        receipt_db.receipts['27'] = receipt
        assert receipt_db.get_receipt('28') == None

    def test_get_with_multiple_stored(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt1 = mock_receipt(
            mocker,
            'Hyvee',
            date(2018, 7, 9),
            datetime(2018, 7, 9, hour=16, minute=28),
            0.99,
            [
                mock_purchased_item(mocker, 'Cabbage', 0.99)
            ]
        )
        receipt2 = mock_receipt(
            mocker,
            'Hyvee',
            date(2018, 7, 10),
            datetime(2018, 7, 10, hour=17, minute=44),
            2.99,
            [
                mock_purchased_item(mocker, 'Gum', 2.99)
            ]
        )
        receipt3 = mock_receipt(
            mocker,
            'Hyvee',
            date(2018, 7, 11),
            datetime(2018, 7, 11, hour=19, minute=0),
            4.99,
            [
                mock_purchased_item(mocker, 'Soap', 4.99)
            ]
        )

        receipt_db.receipts['1'] = receipt1
        receipt_db.receipts['2'] = receipt2
        receipt_db.receipts['3'] = receipt3

        assert receipt_db.get_receipt('2') == receipt2

class TestAddReceipt:
    def test_id(self) -> None:
        receipt_db = ReceiptDatabase()
        receipt_data = {
            'retailer': 'Sears',
            'purchaseDate': '2018-04-30',
            'purchaseTime': '15:08',
            'total': '7.99',
            'items': [
                {
                    'shortDescription': 'Hangers',
                    'price': '7.99'
                }
            ]
        }

        assert receipt_db.add_receipt(receipt_data) == '1'

    def test_retailer(self) -> None:
        receipt_db = ReceiptDatabase()
        retailer = 'Sears'
        receipt_data = {
            'retailer': retailer,
            'purchaseDate': '2018-04-30',
            'purchaseTime': '15:08',
            'total': '29.98',
            'items': [
                {
                    'shortDescription': 'Hangers',
                    'price': '7.99'
                },
                {
                    'shortDescription': 'Shirt',
                    'price': '21.99'
                }
            ]
        }

        receipt_db.add_receipt(receipt_data)
        receipt = receipt_db.receipts['1']
        assert receipt.retailer == retailer

    def test_purchase_date(self) -> None:
        receipt_db = ReceiptDatabase()
        receipt_data = {
            'retailer': 'Sears',
            'purchaseDate': '2018-04-30',
            'purchaseTime': '15:08',
            'total': '29.98',
            'items': [
                {
                    'shortDescription': 'Hangers',
                    'price': '7.99'
                },
                {
                    'shortDescription': 'Shirt',
                    'price': '21.99'
                }
            ]
        }

        receipt_db.add_receipt(receipt_data)
        receipt = receipt_db.receipts['1']
        same_year = receipt.purchase_date.year == 2018
        same_month = receipt.purchase_date.month == 4
        same_day = receipt.purchase_date.day == 30
        assert same_year and same_month and same_day

    def test_purchase_time(self) -> None:
        receipt_db = ReceiptDatabase()
        receipt_data = {
            'retailer': 'Sears',
            'purchaseDate': '2018-04-30',
            'purchaseTime': '15:08',
            'total': '29.98',
            'items': [
                {
                    'shortDescription': 'Hangers',
                    'price': '7.99'
                },
                {
                    'shortDescription': 'Shirt',
                    'price': '21.99'
                }
            ]
        }

        receipt_db.add_receipt(receipt_data)
        receipt = receipt_db.receipts['1']
        same_hour = receipt.purchase_time.hour == 15
        same_minute = receipt.purchase_time.minute == 8
        assert same_hour and same_minute

    def test_total(self) -> None:
        receipt_db = ReceiptDatabase()
        receipt_data = {
            'retailer': 'Sears',
            'purchaseDate': '2018-04-30',
            'purchaseTime': '15:08',
            'total': '29.98',
            'items': [
                {
                    'shortDescription': 'Hangers',
                    'price': '7.99'
                },
                {
                    'shortDescription': 'Shirt',
                    'price': '21.99'
                }
            ]
        }

        receipt_db.add_receipt(receipt_data)
        receipt = receipt_db.receipts['1']
        assert receipt.total_cost == 29.98

    def test_first_item(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt_data = {
            'retailer': 'Sears',
            'purchaseDate': '2018-04-30',
            'purchaseTime': '15:08',
            'total': '29.98',
            'items': [
                {
                    'shortDescription': 'Hangers',
                    'price': '7.99'
                },
                {
                    'shortDescription': 'Shirt',
                    'price': '21.99'
                }
            ]
        }

        item1 = mock_purchased_item(
            mocker,
            receipt_data['items'][0]['shortDescription'],
            float(receipt_data['items'][0]['price'])
        )

        receipt_db.add_receipt(receipt_data)
        first_item = receipt_db.receipts['1'].purchased_items[0]
        assert first_item == item1

    def test_last_item(self, mocker: MockerFixture) -> None:
        receipt_db = ReceiptDatabase()
        receipt_data = {
            'retailer': 'Sears',
            'purchaseDate': '2018-04-30',
            'purchaseTime': '15:08',
            'total': '29.98',
            'items': [
                {
                    'shortDescription': 'Hangers',
                    'price': '7.99'
                },
                {
                    'shortDescription': 'Shirt',
                    'price': '21.99'
                }
            ]
        }

        item2 = mock_purchased_item(
            mocker,
            receipt_data['items'][1]['shortDescription'],
            float(receipt_data['items'][1]['price'])
        )

        receipt_db.add_receipt(receipt_data)
        second_item = receipt_db.receipts['1'].purchased_items[1]
        assert second_item == item2