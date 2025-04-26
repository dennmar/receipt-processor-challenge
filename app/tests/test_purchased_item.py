import pytest

from app.purchased_item import PurchasedItem

class TestMissingKeys:
    def test_missing_desc(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            item = PurchasedItem({
                'price': '123.09'
            })

        error_msg = 'Item in receipt must define the shortDescription key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_misnamed_desc(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            item = PurchasedItem({
                'description': 'Curtains',
                'price': '123.09'
            })

        error_msg = 'Item in receipt must define the shortDescription key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_missing_price(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            item = PurchasedItem({
                'shortDescription': 'Curtains'
            })

        error_msg = 'Item in receipt must define the price key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

    def test_misnamed_price(self) -> None:
        with pytest.raises(KeyError) as excinfo:
            item = PurchasedItem({
                'shortDescription': 'Curtains',
                'cost': '123.09'
            })

        error_msg = 'Item in receipt must define the price key:'
        assert str(excinfo.value.args[0]).startswith(error_msg)

class TestParsePrice:
    EXPECTED_ERROR_MSG = 'Price could not be parsed for item:'

    def create_test_item(self) -> PurchasedItem:
        return PurchasedItem({
            'shortDescription': 'Pear',
            'price': '5.35'
        })

    def test_empty_string(self) -> None:
        item = self.create_test_item()

        with pytest.raises(ValueError) as excinfo:
            item._parse_price('')

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_zero(self) -> None:
        item = self.create_test_item()
        assert item._parse_price('0.00') == 0.00

    def test_under_one_dollar(self) -> None:
        item = self.create_test_item()
        assert item._parse_price('0.77') == 0.77

    def test_normal_price(self) -> None:
        item = self.create_test_item()
        assert item._parse_price('60.34') == 60.34

    def test_non_number(self) -> None:
        item = self.create_test_item()
        price = 'Five'

        with pytest.raises(ValueError) as excinfo:
            item._parse_price(price)

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

    def test_letters_and_numbers(self) -> None:
        item = self.create_test_item()
        price = '1Ab0d.9'

        with pytest.raises(ValueError) as excinfo:
            item._parse_price(price)

        assert str(excinfo.value.args[0]).startswith(self.EXPECTED_ERROR_MSG)

class TestGetShortDescription:
    def test_empty_string(self) -> None:
        item = PurchasedItem({
            'shortDescription': '',
            'price': '1.86'
        })

        assert item.get_short_description() == ''

    def test_normal_desc(self) -> None:
        desc = 'Coke - 12-oz'
        item = PurchasedItem({
            'shortDescription': desc,
            'price': '2.50'
        })

        assert item.get_short_description() == desc

    def test_leading_whitespace(self) -> None:
        desc = '  Macaroni'
        item = PurchasedItem({
            'shortDescription': desc,
            'price': '4.95'
        })

        assert item.get_short_description() == desc

    def test_ending_whitespace(self) -> None:
        desc = 'Cereal      '
        item = PurchasedItem({
            'shortDescription': desc,
            'price': '5.31'
        })

        assert item.get_short_description() == desc

    def test_whitespace_both_ends(self) -> None:
        desc = ' Fruit Loops  '
        item = PurchasedItem({
            'shortDescription': desc,
            'price': '120.35'
        })

        assert item.get_short_description() == desc

class TestGetPrice:
    def test_normal_price(self) -> None:
        item = PurchasedItem({
            'shortDescription': 'Turkey',
            'price': '30.39'
        })

        assert item.get_price() == 30.39

    def test_round_number(self) -> None:
        item = PurchasedItem({
            'shortDescription': 'Firewood',
            'price': '14.00'
        })

        assert item.get_price() == 14.00

    def test_under_one_dollar(self) -> None:
        item = PurchasedItem({
            'shortDescription': 'Cookie',
            'price': '0.49'
        })

        assert item.get_price() == 0.49

    def test_zero(self) -> None:
        item = PurchasedItem({
            'shortDescription': 'Watermelon',
            'price': '0.00'
        })

        assert item.get_price() == 0.00