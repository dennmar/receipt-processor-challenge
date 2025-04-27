from flask.testing import FlaskClient

class TestStoreReceipt:
    ROUTE = '/receipts/process'

    def test_valid_store_resp_code(self, client: FlaskClient) -> None:
        resp = client.post(self.ROUTE, json={
            'retailer': 'Target',
            'purchaseDate': '2022-01-02',
            'purchaseTime': '13:13',
            'total': '1.25',
            'items': [
                {'shortDescription': 'Pepsi - 12-oz', 'price': '1.25'}
            ]
        })

        assert resp.status_code == 200

    def test_valid_store_data(self, client: FlaskClient) -> None:
        resp = client.post(self.ROUTE, json={
            'retailer': 'Target',
            'purchaseDate': '2022-01-02',
            'purchaseTime': '13:13',
            'total': '1.25',
            'items': [
                {'shortDescription': 'Pepsi - 12-oz', 'price': '1.25'}
            ]
        })

        assert resp.json == {'id': '1'}

    def test_missing_key_resp_code(self, client: FlaskClient) -> None:
        resp = client.post(self.ROUTE, json={
            'retailer': 'Target',
            'purchaseDate': '2022-01-02',
            'total': '1.25',
            'items': [
                {'shortDescription': 'Pepsi - 12-oz', 'price': '1.25'}
            ]
        })

        assert resp.status_code == 400

    def test_misnamed_key_resp_code(self, client: FlaskClient) -> None:
        resp = client.post(self.ROUTE, json={
            'retailer': 'Target',
            'purchasedate': '2022-01-02',
            'purchaseTime': '13:13',
            'total': '1.25',
            'items': [
                {'shortDescription': 'Pepsi - 12-oz', 'price': '1.25'}
            ]
        })

        assert resp.status_code == 400

    def test_invalid_value(self, client: FlaskClient) -> None:
        resp = client.post(self.ROUTE, json={
            'retailer': 'Target',
            'purchaseDate': '2022-30-72',
            'purchaseTime': '13:13',
            'total': '1.25',
            'items': [
                {'shortDescription': 'Pepsi - 12-oz', 'price': '1.25'}
            ]
        })

        assert resp.status_code == 400

    def test_multiple_stores_resp_code(self, client: FlaskClient) -> None:
        client.post(self.ROUTE, json={
            'retailer': 'Toys 'R' Us',
            'purchaseDate': '2019-01-30',
            'purchaseTime': '07:55',
            'total': '16.23',
            'items': [
                {'shortDescription': 'Puzzle', 'price': '16.23'}
            ]
        })
        client.post(self.ROUTE, json={
            'retailer': 'McDonald\'s',
            'purchaseDate': '2019-02-02',
            'purchaseTime': '12:32',
            'total': '4.98',
            'items': [
                {'shortDescription': 'Coffee', 'price': '4.98'}
            ]
        })
        resp = client.post(self.ROUTE, json={
            'retailer': 'Hatty',
            'purchaseDate': '2020-11-15',
            'purchaseTime': '22:31',
            'total': '1104.24',
            'items': [
                {'shortDescription': 'Top Hat', 'price': '1104.25'}
            ]
        })

        assert resp.status_code == 200

    def test_multiple_stores_data(self, client: FlaskClient) -> None:
        client.post(self.ROUTE, json={
            'retailer': 'Toys 'R' Us',
            'purchaseDate': '2019-01-30',
            'purchaseTime': '07:55',
            'total': '16.23',
            'items': [
                {'shortDescription': 'Puzzle', 'price': '16.23'}
            ]
        })
        client.post(self.ROUTE, json={
            'retailer': 'McDonald\'s',
            'purchaseDate': '2019-02-02',
            'purchaseTime': '12:32',
            'total': '4.98',
            'items': [
                {'shortDescription': 'Coffee', 'price': '4.98'}
            ]
        })
        resp = client.post(self.ROUTE, json={
            'retailer': 'Hatty',
            'purchaseDate': '2020-11-15',
            'purchaseTime': '22:31',
            'total': '1104.24',
            'items': [
                {'shortDescription': 'Top Hat', 'price': '1104.25'}
            ]
        })

        assert resp.json == {'id': '3'}

    def test_multiple_same_resp_code(self, client: FlaskClient) -> None:
        receipt_json = {
            'retailer': 'Sports Authority',
            'purchaseDate': '2024-12-05',
            'purchaseTime': '13:00',
            'total': '202.50',
            'items': [
                {'shortDescription': 'Boxing Gloves', 'price': '54.16'},
                {'shortDescription': 'Training Pads', 'price': '23.64'},
                {'shortDescription': 'Punching Bag', 'price': '124.70'}
            ]
        }
        
        client.post(self.ROUTE, json=receipt_json)
        client.post(self.ROUTE, json=receipt_json)
        client.post(self.ROUTE, json=receipt_json)
        client.post(self.ROUTE, json=receipt_json)
        client.post(self.ROUTE, json=receipt_json)
        resp = client.post(self.ROUTE, json=receipt_json)

        assert resp.status_code == 200

    def test_multiple_same_data(self, client: FlaskClient) -> None:
        receipt_json = {
            'retailer': 'Sports Authority',
            'purchaseDate': '2024-12-05',
            'purchaseTime': '13:00',
            'total': '202.50',
            'items': [
                {'shortDescription': 'Boxing Gloves', 'price': '54.16'},
                {'shortDescription': 'Training Pads', 'price': '23.64'},
                {'shortDescription': 'Punching Bag', 'price': '124.70'}
            ]
        }
        
        client.post(self.ROUTE, json=receipt_json)
        client.post(self.ROUTE, json=receipt_json)
        client.post(self.ROUTE, json=receipt_json)
        client.post(self.ROUTE, json=receipt_json)
        client.post(self.ROUTE, json=receipt_json)
        resp = client.post(self.ROUTE, json=receipt_json)

        assert resp.json == {'id': '6'}

class TestGetPoints:
    ADD_ROUTE = '/receipts/process'

    def test_example1_resp_code(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'Target',
            'purchaseDate': '2022-01-01',
            'purchaseTime': '13:01',
            'items': [
                {
                'shortDescription': 'Mountain Dew 12PK',
                'price': '6.49'
                },{
                'shortDescription': 'Emils Cheese Pizza',
                'price': '12.25'
                },{
                'shortDescription': 'Knorr Creamy Chicken',
                'price': '1.26'
                },{
                'shortDescription': 'Doritos Nacho Cheese',
                'price': '3.35'
                },{
                'shortDescription': '   Klarbrunn 12-PK 12 FL OZ  ',
                'price': '12.00'
                }
            ],
            'total': '35.35'
        })
        resp = client.get('/receipts/1/points')

        assert resp.status_code == 200

    def test_example1_data(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'Target',
            'purchaseDate': '2022-01-01',
            'purchaseTime': '13:01',
            'items': [
                {
                'shortDescription': 'Mountain Dew 12PK',
                'price': '6.49'
                },{
                'shortDescription': 'Emils Cheese Pizza',
                'price': '12.25'
                },{
                'shortDescription': 'Knorr Creamy Chicken',
                'price': '1.26'
                },{
                'shortDescription': 'Doritos Nacho Cheese',
                'price': '3.35'
                },{
                'shortDescription': '   Klarbrunn 12-PK 12 FL OZ  ',
                'price': '12.00'
                }
            ],
            'total': '35.35'
        })
        resp = client.get('/receipts/1/points')

        assert resp.json == {'points': 28}

    def test_example2_resp_code(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'M&M Corner Market',
            'purchaseDate': '2022-03-20',
            'purchaseTime': '14:33',
            'items': [
                {
                    'shortDescription': 'Gatorade',
                    'price': '2.25'
                },
                {
                    'shortDescription': 'Gatorade',
                    'price': '2.25'
                },
                {
                    'shortDescription': 'Gatorade',
                    'price': '2.25'
                },
                {
                    'shortDescription': 'Gatorade',
                    'price': '2.25'
                }
            ],
            'total': '9.00'
        })
        resp = client.get('/receipts/1/points')

        assert resp.status_code == 200

    def test_example2_data(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'M&M Corner Market',
            'purchaseDate': '2022-03-20',
            'purchaseTime': '14:33',
            'items': [
                {
                    'shortDescription': 'Gatorade',
                    'price': '2.25'
                },
                {
                    'shortDescription': 'Gatorade',
                    'price': '2.25'
                },
                {
                    'shortDescription': 'Gatorade',
                    'price': '2.25'
                },
                {
                    'shortDescription': 'Gatorade',
                    'price': '2.25'
                }
            ],
            'total': '9.00'
        })
        resp = client.get('/receipts/1/points')

        assert resp.json == {'points': 109}

    def test_example3_resp_code(self, client: FlaskClient) -> None:
        name = 'Jim Jr. and Rhino\'s Frozen Grill & Hot Lemonade v3.0'
        client.post(self.ADD_ROUTE, json={
            'retailer': name,
            'purchaseDate': '2025-12-31',
            'purchaseTime': '16:00',
            'items': [
                {
                    'shortDescription': 'Lemonade Extra Hot ',
                    'price': '52.75'
                }
            ],
            'total': '52.75'
        })
        resp = client.get('receipts/1/points')

        assert resp.status_code == 200

    def test_example3_data(self, client: FlaskClient) -> None:
        name = 'Jim Jr. and Rhino\'s Frozen Grill & Hot Lemonade v3.0'
        client.post(self.ADD_ROUTE, json={
            'retailer': name,
            'purchaseDate': '2025-12-31',
            'purchaseTime': '16:00',
            'items': [
                {
                    'shortDescription': 'Lemonade Extra Hot ',
                    'price': '52.75'
                }
            ],
            'total': '52.75'
        })
        resp = client.get('receipts/1/points')

        assert resp.json == {'points': 81}

    def test_example4_resp_code(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'Plushie Store  ',
            'purchaseDate': '1944-10-27',
            'purchaseTime': '14:00',
            'items': [
                {
                    'shortDescription': '  Stuffed Teddy Bear     ',
                    'price': '230.28'
                },
                {
                    'shortDescription': ' Stuffed Dragon',
                    'price': '129.00'
                },
                {
                    'shortDescription': 'Stuffed Pig #12',
                    'price': '10.24'
                },
                {
                    'shortDescription': 'Stuffed Pig #249',
                    'price': '28.23'
                },
                {
                    'shortDescription': 'Cotton',
                    'price': '57.04'
                },
                {
                    'shortDescription': 'Limited Edition Red Fish',
                    'price': '10392.46'
                }
            ],
            'total': '10847.25'
        })
        resp = client.get('receipts/1/points')

        assert resp.status_code == 200

    def test_example4_data(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'Plushie Store  ',
            'purchaseDate': '1944-10-27',
            'purchaseTime': '14:00',
            'items': [
                {
                    'shortDescription': '  Stuffed Teddy Bear     ',
                    'price': '230.28'
                },
                {
                    'shortDescription': ' Stuffed Dragon',
                    'price': '129.00'
                },
                {
                    'shortDescription': 'Stuffed Pig #12',
                    'price': '10.24'
                },
                {
                    'shortDescription': 'Stuffed Pig #249',
                    'price': '28.23'
                },
                {
                    'shortDescription': 'Cotton',
                    'price': '57.04'
                },
                {
                    'shortDescription': 'Limited Edition Red Fish',
                    'price': '10392.46'
                }
            ],
            'total': '10847.25'
        })
        resp = client.get('receipts/1/points')

        assert resp.json == {'points': 2199}

    def test_example5_resp_code(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'Norm\'s 100% Organic Barn',
            'purchaseDate': '2021-08-30',
            'purchaseTime': '14:01',
            'items': [],
            'total': '0.00'
        })
        resp = client.get('receipts/1/points')

        assert resp.json == {'points': 104}

    def test_empty_db_resp_code(self, client: FlaskClient) -> None:
        resp = client.get('receipts/1/points')
        assert resp.status_code == 404

    def test_empty_db_data(self, client: FlaskClient) -> None:
        resp = client.get('receipts/1/points')
        assert resp.text == 'No receipt found with the id of 1'

    def test_invalid_id_data(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'Norm\'s 100% Organic Barn',
            'purchaseDate': '2021-08-30',
            'purchaseTime': '14:01',
            'items': [],
            'total': '0.00'
        })
        resp = client.get('receipts/2/points')

        assert resp.status_code == 404

    def test_invalid_id_data(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'Norm\'s 100% Organic Barn',
            'purchaseDate': '2021-08-30',
            'purchaseTime': '14:01',
            'items': [],
            'total': '0.00'
        })
        resp = client.get('receipts/2/points')

        assert resp.text == 'No receipt found with the id of 2'

    def test_multiple_store_score1(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'General Store',
            'purchaseDate': '2023-02-15',
            'purchaseTime': '15:59',
            'items': [
                {'shortDescription': ' Coke Zero (New)', 'price': '14.78'}
            ],
            'total': '14.78'
        })
        client.post(self.ADD_ROUTE, json={
            'retailer': 'A',
            'purchaseDate': '2023-05-12',
            'purchaseTime': '23:04',
            'items': [
                {'shortDescription': 'Candles', 'price': '100.20'}
            ],
            'total': '100.20'
        })
        client.post(self.ADD_ROUTE, json={
            'retailer': '7-11',
            'purchaseDate': '2024-01-03',
            'purchaseTime': '07:20',
            'items': [
                {'shortDescription': ' Lighter ', 'price': '150.00'},
                {'shortDescription': 'Cigarettes', 'price': '25.00'}
            ],
            'total': '175.00'
        })
        resp = client.get('receipts/1/points')

        assert resp.json == {'points': 31}

    def test_multiple_store_score2(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'General Store',
            'purchaseDate': '2023-02-15',
            'purchaseTime': '15:59',
            'items': [
                {'shortDescription': ' Coke Zero (New)', 'price': '14.78'}
            ],
            'total': '14.78'
        })
        client.post(self.ADD_ROUTE, json={
            'retailer': 'A',
            'purchaseDate': '2023-05-12',
            'purchaseTime': '23:04',
            'items': [
                {'shortDescription': 'Candles', 'price': '100.20'}
            ],
            'total': '100.20'
        })
        client.post(self.ADD_ROUTE, json={
            'retailer': '7-11',
            'purchaseDate': '2024-01-03',
            'purchaseTime': '07:20',
            'items': [
                {'shortDescription': ' Lighter ', 'price': '150.00'},
                {'shortDescription': 'Cigarettes', 'price': '25.00'}
            ],
            'total': '175.00'
        })
        resp = client.get('receipts/2/points')

        assert resp.json == {'points': 1}

    def test_multiple_store_score3(self, client: FlaskClient) -> None:
        client.post(self.ADD_ROUTE, json={
            'retailer': 'General Store',
            'purchaseDate': '2023-02-15',
            'purchaseTime': '15:59',
            'items': [
                {'shortDescription': ' Coke Zero (New)', 'price': '14.78'}
            ],
            'total': '14.78'
        })
        client.post(self.ADD_ROUTE, json={
            'retailer': 'A',
            'purchaseDate': '2023-05-12',
            'purchaseTime': '23:04',
            'items': [
                {'shortDescription': 'Candles', 'price': '100.20'}
            ],
            'total': '100.20'
        })
        client.post(self.ADD_ROUTE, json={
            'retailer': '7-11',
            'purchaseDate': '2024-01-03',
            'purchaseTime': '07:20',
            'items': [
                {'shortDescription': ' Lighter ', 'price': '150.00'},
                {'shortDescription': 'Cigarettes', 'price': '25.00'}
            ],
            'total': '175.00'
        })
        resp = client.get('receipts/3/points')

        assert resp.json == {'points': 89}