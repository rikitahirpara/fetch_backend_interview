import unittest
from fetch_receipt_processor import app, calculate_points

class TestReceiptsAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_process_receipts(self):
        payload = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Item 1", "price": "5.00"},
                {"shortDescription": "Item 2", "price": "10.00"}
            ],
            "total": "15.00"
        }

        response = self.app.post('/receipts/process', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data.get('id'))

    def test_process_receipts_invalid_date(self):
        payload = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Item 1", "price": "5.00"},
                {"shortDescription": "Item 2", "price": "10.00"}
            ],
            "total": "15.00"
        }

        response = self.app.post('/receipts/process', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)

    def test_process_receipts_invalid_time(self):
        payload = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13",
            "items": [
                {"shortDescription": "Item 1", "price": "5.00"},
                {"shortDescription": "Item 2", "price": "10.00"}
            ],
            "total": "15.00"
        }

        response = self.app.post('/receipts/process', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)


    def test_get_points(self):
        payload = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Item 1", "price": "5.00"},
                {"shortDescription": "Item 2", "price": "10.00"}
            ],
            "total": "15.00"
        }

        response = self.app.post('/receipts/process', json=payload)
        data = response.get_json()

        # Assuming you have a known receipt ID from a previous test
        receipt_id = data.get('id')

        response = self.app.get(f'/receipts/{receipt_id}/points')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('points'))

    def test_points_calculation_example1(self):
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
            ],
            "total": "35.35"
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 28)

    def test_points_calculation_example2(self):
        receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"}
            ],
            "total": "9.00"
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 109)

    def test_points_calculation_example_morning(self):
        receipt = {
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ]
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 15)

    def test_points_calculation_example_simple(self):
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 31)

if __name__ == '__main__':
    unittest.main()