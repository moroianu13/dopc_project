from django.shortcuts import render
from django.urls import path
from django.http import JsonResponse, HttpResponse
import requests
import math


def welcome(request):
    return HttpResponse("<h1>Welcome to the Delivery Order Price Calculator</h1>")


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def fetch_static_data(venue_slug):
    url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_dynamic_data(venue_slug):
    url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def calculate_price(request):
    venue_slug = request.GET.get('venue_slug')
    cart_value = int(request.GET.get('cart_value'))
    user_lat = float(request.GET.get('user_lat'))
    user_lon = float(request.GET.get('user_lon'))

    try:
        static_data = fetch_static_data(venue_slug)
        dynamic_data = fetch_dynamic_data(venue_slug)
    except requests.exceptions.RequestException:
        return JsonResponse({"error": "Unable to fetch venue data"}, status=400)

    venue_coords = static_data['venue_raw']['location']['coordinates']
    venue_lon, venue_lat = venue_coords

    distance = haversine(user_lat, user_lon, venue_lat, venue_lon)

    order_min_no_surcharge = dynamic_data['venue_raw']['delivery_specs']['order_minimum_no_surcharge']
    base_price = dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['base_price']
    distance_ranges = dynamic_data['venue_raw']['delivery_specs']['delivery_pricing']['distance_ranges']

    surcharge = max(0, order_min_no_surcharge - cart_value)

    delivery_fee = base_price
    valid_range = False
    for range_data in distance_ranges:
    # If the max is 0, treat that as "no upper limit."
        if range_data['max'] == 0:
        # Then we only match if distance >= range_data['min']
            if distance >= range_data['min']:
                delivery_fee += range_data['a'] + round(range_data['b'] * distance / 10)
                valid_range = True
                break
        else:
        # Standard lower/upper bound check
            if range_data['min'] <= distance < range_data['max']:
                delivery_fee += range_data['a'] + round(range_data['b'] * distance / 10)
                valid_range = True
                break

    if not valid_range:
        return JsonResponse({"error": "Delivery not possible for this distance"}, status=400)


    total_price = cart_value + surcharge + delivery_fee

    # Debugging prints
    print(f"Calculated distance: {distance}")
    print(f"Distance ranges: {distance_ranges}")

    return JsonResponse({
        "total_price": total_price,
        "small_order_surcharge": surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": delivery_fee,
            "distance": round(distance)
        }
    })


# URL patterns
urlpatterns = [
    path('', welcome, name='welcome'),
    path('api/v1/delivery-order-price', calculate_price, name='calculate_price'),
]
