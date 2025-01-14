from django.test import TestCase, Client
from django.urls import reverse
from dopc.views import haversine  # Correctly import from the app
from unittest.mock import patch


# Tests for haversine function
class HaversineTestCase(TestCase):
    def test_haversine_distance(self):
        lat1, lon1 = 52.5200, 13.4050  # Berlin coordinates
        lat2, lon2 = 52.5206, 13.4096  # Slightly different Berlin coordinates
        distance = haversine(lat1, lon1, lat2, lon2)
        self.assertAlmostEqual(distance, 318, delta=5)  # Approximate distance in meters


# Mocked static and dynamic API responses
mock_static_data = {
    "venue_raw": {
        "location": {
            "coordinates": [13.4050, 52.5200]  # Berlin coordinates
        }
    }
}

mock_dynamic_data = {
    "venue_raw": {
        "delivery_specs": {
            "order_minimum_no_surcharge": 1000,
            "delivery_pricing": {
                "base_price": 190,
                "distance_ranges": [
                    {"min": 0, "max": 5000, "a": 0, "b": 1, "flag": None},
                ]
            }
        }
    }
}


# Tests for calculate_price view
class CalculatePriceTestCase(TestCase):
    @patch('dopc.views.fetch_static_data', return_value=mock_static_data)
    @patch('dopc.views.fetch_dynamic_data', return_value=mock_dynamic_data)
    def test_calculate_price_success(self, mock_fetch_static, mock_fetch_dynamic):
        client = Client()
        url = reverse('calculate_price')
        params = {
            'venue_slug': 'home-assignment-venue-berlin',
            'cart_value': 1000,
            'user_lat': 52.5200,
            'user_lon': 13.4050
        }
        response = client.get(url, params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_price'], 1190)
        self.assertEqual(data['small_order_surcharge'], 0)
        self.assertEqual(data['delivery']['fee'], 190)
        self.assertEqual(data['delivery']['distance'], 0)

    @patch('dopc.views.fetch_static_data', return_value=mock_static_data)
    @patch('dopc.views.fetch_dynamic_data', return_value=mock_dynamic_data)
    def test_calculate_price_invalid_distance(self, mock_fetch_static, mock_fetch_dynamic):
        client = Client()
        url = reverse('calculate_price')
        params = {
            'venue_slug': 'home-assignment-venue-berlin',
            'cart_value': 1000,
            'user_lat': 60.0000,  # Far away latitude
            'user_lon': 25.0000   # Far away longitude
        }
        response = client.get(url, params)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['error'], "Delivery not possible for this distance")
