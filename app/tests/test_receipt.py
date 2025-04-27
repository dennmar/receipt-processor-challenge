from datetime import date
import pytest
from pytest_mock import MockerFixture

from app.receipt import Receipt
from app.tests.helpers.mockers import mock_purchased_item

def create_test_receipt() -> Receipt:
    return Receipt({
        'retailer': 'Forever 21',
        'purchaseDate': '2021-02-21',
        'purchaseTime': '14:46',
        'items': [
            {
                'shortDescription': 'Jeans',
                'price': '35.78'
            },
            {
                'shortDescription': 'Belt',
                'price': '18.30'
            }
        ],
        'total': '54.08'
    })

class TestMissingKeys:
    def test_missing_retailer(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'purchaseDate': '1955-03-10',
                'purchaseTime': '08:36',
                'items': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ],
                'total': '0.99'
            })

        error_msg = 'Receipt must define the retailer key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_misnamed_retailer(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'store': 'Home Depot',
                'purchaseDate': '1955-03-10',
                'purchaseTime': '08:36',
                'items': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ],
                'total': '0.99'
            })

        error_msg = 'Receipt must define the retailer key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_missing_date(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'retailer': 'Home Depot',
                'purchaseTime': '08:36',
                'items': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ],
                'total': '0.99'
            })

        error_msg = 'Receipt must define the purchaseDate key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_misnamed_date(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'retailer': 'Home Depot',
                'date': '1955-03-10',
                'purchaseTime': '08:36',
                'items': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ],
                'total': '0.99'
            })

        error_msg = 'Receipt must define the purchaseDate key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_missing_time(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'retailer': 'Home Depot',
                'purchaseDate': '1955-03-10',
                'items': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ],
                'total': '0.99'
            })

        error_msg = 'Receipt must define the purchaseTime key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_misnamed_time(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'retailer': 'Home Depot',
                'purchaseDate': '1955-03-10',
                'time': '08:36',
                'items': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ],
                'total': '0.99'
            })

        error_msg = 'Receipt must define the purchaseTime key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_missing_items(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'retailer': 'Home Depot',
                'purchaseDate': '1955-03-10',
                'purchaseTime': '08:36',
                'total': '0.99'
            })

        error_msg = 'Receipt must define the items key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_misnamed_items(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'retailer': 'Home Depot',
                'purchaseDate': '1955-03-10',
                'purchaseTime': '08:36',
                'item': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ],
                'total': '0.99'
            })

        error_msg = 'Receipt must define the items key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_missing_total(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'retailer': 'Home Depot',
                'purchaseDate': '1955-03-10',
                'purchaseTime': '08:36',
                'items': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ]
            })

        error_msg = 'Receipt must define the total key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_misnamed_total(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            receipt = Receipt({
                'retailer': 'Home Depot',
                'purchaseDate': '1955-03-10',
                'purchaseTime': '08:36',
                'item': [
                    {
                        'shortDescription': 'Brick',
                        'price': '0.99'
                    } 
                ],
                'cost': '0.99'
            })

        error_msg = 'Receipt must define the total key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

class TestParseDate:
    EXPECTED_ERROR_MSG = 'Receipt purchase date does not match "YYYY-MM-DD":' 

    def test_normal_date(self) -> None:
        receipt = create_test_receipt()
        assert receipt._parse_date('2041-07-24') == date(2041, 7, 24)

    def test_empty_string(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_date('')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_missing_year(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_date('01-31')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_missing_month(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_date('1983-31')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_missing_day(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_date('1983-01')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_invalid_month(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_date('1983-13-22')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_invalid_day(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_date('1983-08-78')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_invalid_string(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_date('Jan. 1, 1900')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

class TestParseTime:
    EXPECTED_ERROR_MSG = 'Receipt purchase time does not match "H:M":'

    def test_am_time(self) -> None:
        receipt = create_test_receipt()
        time = receipt._parse_time('03:12')
        assert time.hour == 3 and time.minute == 12

    def test_pm_time(self) -> None:
        receipt = create_test_receipt()
        time = receipt._parse_time('16:45')
        assert time.hour == 16 and time.minute == 45

    def test_hour_zero(self) -> None:
        receipt = create_test_receipt()
        time = receipt._parse_time('00:32')
        assert time.hour == 0 and time.minute == 32

    def test_minute_zero(self) -> None:
        receipt = create_test_receipt()
        time = receipt._parse_time('23:00')
        assert time.hour == 23 and time.minute == 0

    def test_invalid_hour(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_time('24:10')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_invalid_minute(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_time('13:60')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_incomplete_string(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_time('14')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)       

    def test_invalid_string(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_time('Midnight')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

class TestParseTotalCost:
    EXPECTED_ERROR_MSG = 'Total could not be parsed for receipt:'

    def test_normal_cost(self) -> None:
        receipt = create_test_receipt()
        assert receipt._parse_total_cost('132.86') == 132.86

    def test_under_one_dollar(self) -> None:
        receipt = create_test_receipt()
        assert receipt._parse_total_cost('0.01') == 0.01

    def test_zero(self) -> None:
        receipt = create_test_receipt()
        assert receipt._parse_total_cost('0.00') == 0.00

    def test_empty_string(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_total_cost('')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_non_number(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_total_cost('Two')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_letters_and_numbers(self) -> None:
        receipt = create_test_receipt()

        with pytest.raises(ValueError) as excinfo:
            receipt._parse_total_cost('28s.4U')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

class TestParsePurchasedItems:
    def test_zero_items(self) -> None:
        receipt = create_test_receipt()
        assert receipt._parse_purchased_items([]) == []

    def test_one_item(self, mocker: MockerFixture) -> None:
        receipt = create_test_receipt()
        items = receipt._parse_purchased_items([
            {
                'shortDescription': 'Beer',
                'price': '15.42'
            }
        ])

        expected_items = [
            mock_purchased_item(
                mocker,
                'Beer',
                15.42
            )
        ]

        assert items == expected_items

    def test_multiple_items(self, mocker: MockerFixture) -> None:
        receipt = create_test_receipt()
        items = receipt._parse_purchased_items([
            {
                'shortDescription': 'Smores',
                'price': '8.67'
            },
            {
                'shortDescription': 'Tent',
                'price': '143.50'
            },
            {
                'shortDescription': 'Thermos',
                'price': '33.90'
            }
        ])

        expected_items = [
            mock_purchased_item(mocker, 'Smores', 8.67),
            mock_purchased_item(mocker, 'Tent', 143.50),
            mock_purchased_item(mocker, 'Thermos', 33.90)
        ]

        assert items == expected_items

class TestGetRetailer:
    def test_normal_name(self) -> None:
        retailer = 'Adoption Shelter'
        receipt = Receipt({
            'retailer': retailer,
            'purchaseDate': '2013-06-12',
            'purchaseTime': '11:08',
            'items': [
                {
                    'shortDescription': 'Rhino',
                    'price': '124.45'
                },
                {
                    'shortDescription': 'Panda',
                    'price': '4568.32'
                }
            ],
            'total': '4692.77'
        })

        assert receipt.get_retailer() == retailer

class TestGetPurchaseDate:
    def test_single_digit_month(self) -> None:
        receipt = Receipt({
            'retailer': 'Antique Shop',
            'purchaseDate': '1943-04-24',
            'purchaseTime': '15:09',
            'items': [
                {
                    'shortDescription': 'Lamp',
                    'price': '15.65'
                }
            ],
            'total': '15.65'
        })

        assert receipt.get_purchase_date() == date(1943, 4, 24)

    def test_double_digit_month(self) -> None:
        receipt = Receipt({
            'retailer': 'Antique Shop',
            'purchaseDate': '1943-10-24',
            'purchaseTime': '15:09',
            'items': [
                {
                    'shortDescription': 'Lamp',
                    'price': '15.65'
                }
            ],
            'total': '15.65'
        })

        assert receipt.get_purchase_date() == date(1943, 10, 24)

    def test_single_digit_day(self) -> None:
        receipt = Receipt({
            'retailer': 'Antique Shop',
            'purchaseDate': '1943-12-01',
            'purchaseTime': '15:09',
            'items': [
                {
                    'shortDescription': 'Lamp',
                    'price': '15.65'
                }
            ],
            'total': '15.65'
        })

        assert receipt.get_purchase_date() == date(1943, 12, 1)

    def test_double_digit_day(self) -> None:
        receipt = Receipt({
            'retailer': 'Antique Shop',
            'purchaseDate': '1943-10-31',
            'purchaseTime': '15:09',
            'items': [
                {
                    'shortDescription': 'Lamp',
                    'price': '15.65'
                }
            ],
            'total': '15.65'
        })

        assert receipt.get_purchase_date() == date(1943, 10, 31)

class TestGetPurchaseTime:
    def test_single_digit_hour(self) -> None:
        receipt = Receipt({
            'retailer': 'Vending Machine',
            'purchaseDate': '2001-08-19',
            'purchaseTime': '03:10',
            'items': [
                {
                    'shortDescription': 'Granola Bar',
                    'price': '2.97'
                }
            ],
            'total': '2.97'
        })

        assert receipt.get_purchase_time().hour == 3

    def test_double_digit_hour(self) -> None:
        receipt = Receipt({
            'retailer': 'Vending Machine',
            'purchaseDate': '2001-08-19',
            'purchaseTime': '20:10',
            'items': [
                {
                    'shortDescription': 'Granola Bar',
                    'price': '2.97'
                }
            ],
            'total': '2.97'
        })

        assert receipt.get_purchase_time().hour == 20

    def test_single_digit_minute(self) -> None:
        receipt = Receipt({
            'retailer': 'Vending Machine',
            'purchaseDate': '2001-08-19',
            'purchaseTime': '21:08',
            'items': [
                {
                    'shortDescription': 'Granola Bar',
                    'price': '2.97'
                }
            ],
            'total': '2.97'
        })

        assert receipt.get_purchase_time().minute == 8

    def test_double_digit_minute(self) -> None:
        receipt = Receipt({
            'retailer': 'Vending Machine',
            'purchaseDate': '2001-08-19',
            'purchaseTime': '17:51',
            'items': [
                {
                    'shortDescription': 'Granola Bar',
                    'price': '2.97'
                }
            ],
            'total': '2.97'
        })

        assert receipt.get_purchase_time().minute == 51

class TestGetTotalCost:
    def test_zero(self) -> None:
        receipt = Receipt({
            'retailer': 'Hobby Lobby',
            'purchaseDate': '2008-12-03',
            'purchaseTime': '02:39',
            'items': [
                {
                    'shortDescription': 'Couch',
                    'price': '0.00'
                }
            ],
            'total': '0.00'
        })

        assert receipt.get_total_cost() == 0.00

    def test_normal(self) -> None:
        receipt = Receipt({
            'retailer': 'Hobby Lobby',
            'purchaseDate': '2008-12-03',
            'purchaseTime': '02:39',
            'items': [
                {
                    'shortDescription': 'Couch',
                    'price': '205.51'
                }
            ],
            'total': '205.51'
        })

        assert receipt.get_total_cost() == 205.51

class TestGetPurchasedItems:
    def test_zero_items(self) -> None:
        receipt = Receipt({
            'retailer': 'Lemonade Stand',
            'purchaseDate': '2080-02-23',
            'purchaseTime': '12:34',
            'items': [],
            'total': '0.00'
        })

        assert receipt.get_purchased_items() == []

    def test_one_item(self, mocker: MockerFixture) -> None:
        receipt = Receipt({
            'retailer': 'Hot Dog Stand',
            'purchaseDate': '2130-03-06',
            'purchaseTime': '19:48',
            'items': [
                {
                    'shortDescription': 'Hot Dog',
                    'price': '2.90'
                }
            ],
            'total': '2.90'
        })

        expected_items = [
            mock_purchased_item(mocker, 'Hot Dog', 2.90)
        ]

        assert receipt.get_purchased_items() == expected_items

    def test_multiple_items(self, mocker: MockerFixture) -> None:
        receipt = Receipt({
            'retailer': 'Kay',
            'purchaseDate': '2037-07-14',
            'purchaseTime': '09:13',
            'items': [
                {
                    'shortDescription': 'Ring',
                    'price': '469.47'
                },
                {
                    'shortDescription': 'Bracelet',
                    'price': '326.71'
                },
                {
                    'shortDescription': 'Necklace',
                    'price': '283.88'
                },
            ],
            'total': '1080.06'
        })

        expected_items = [
            mock_purchased_item(mocker, 'Ring', 469.47),
            mock_purchased_item(mocker, 'Bracelet', 326.71),
            mock_purchased_item(mocker, 'Necklace', 283.88)
        ]

        assert receipt.get_purchased_items() == expected_items