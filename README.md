# Delivery Order Price Calculator (DOPC)

A Django-based project that calculates delivery pricing for orders based on:
- Cart value
- Distance ranges
- Small-order surcharges

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)


---

## Features

- **Distance Calculation**: Uses the Haversine formula to accurately compute distances.
- **Dynamic Pricing**: Supports different distance ranges, surcharges, and base fees.
- **Error Handling**: Returns proper HTTP status codes (e.g., 400 for invalid distances).

---

## Requirements

- Python 3.10+  
- Django 3.2+ (or whichever version you’re using)  
- Other dependencies as listed in `requirements.txt` (if any)

---

## Installation

1. **Clone the repository**:
   
2. **Create and activate a virtual environment**:
  
- python -m venv venv
- source venv/bin/activate  # Linux/Mac
- venv\Scripts\activate     # Windows


3. **Install dependencies**:

- pip install -r requirements.txt

## Running the Project

1. python manage.py migrate

**Run the development server**:

2. python manage.py runserver


3. **Access the application by navigating to**:

- http://127.0.0.1:8000/

## Testing

1. **Run all tests**:

- python manage.py test

2. **You should see output similar to**:

- Creating test database...
- Ran X tests in Y seconds
- OK

## API Endpoints

1. **Calculate Delivery Price**

- GET /api/v1/delivery-order-price


**Query Parameters:**

- venue_slug (string): The venue identifier.
- cart_value (int): Cart value in cents.
- user_lat (float): User’s latitude.
- user_lon (float): User’s longitude.


## Sample Request:

- GET /api/v1/delivery-order-price?venue_slug=my_venue&cart_value=2000&user_lat=52.5200&user_lon=13.4050


## Sample Response:

**{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 0
  }
}**





