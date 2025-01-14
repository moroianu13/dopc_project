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
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [License](#license)

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
   ```bash
   git clone https://github.com/yourusername/dopc_project.git
   cd dopc_project


2. **Create and activate a virtual environment**:
  '''bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows


3. **Install dependencies**:

pip install -r requirements.txt

## Running the Project

1. **Set up the Django database (if needed):
    python manage.py migrate

2. **Run the development server**:

python manage.py runserver


3. **Access the application by navigating to**:

http://127.0.0.1:8000/

## Testing

1. **Run all tests**:

python manage.py test

2. **You should see output similar to**:

Creating test database...
Ran X tests in Y seconds
OK

## Project Structure

##### Below is a sample directory layout. Your exact structure may vary.

.
├── dopc_project/
│   ├── dopc/                     # Main Django app
│   │   ├── views.py              # Core views (distance calculations, etc.)
│   │   ├── tests.py              # Unit tests
│   │   ├── ...
│   ├── dopc_project/
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Project URL routing
│   │   ├── wsgi.py               # WSGI configuration
│   │   └── ...
│   ├── manage.py
├── venv/                         # Virtual environment (ignored by .gitignore)
├── requirements.txt
├── README.md                     # This file
└── .gitignore


## API Endpoints

1. **Welcome (root URL)**

GET /
- Returns a simple welcome message: "Welcome to the Delivery Order Price Calculator"

2. ** Calculate Delivery Price**

GET /api/v1/delivery-order-price


Query Parameters:

- venue_slug (string): The venue identifier.
- cart_value (int): Cart value in cents.
- user_lat (float): User’s latitude.
- user_lon (float): User’s longitude.


## Sample Request:

Sample Request:

GET /api/v1/delivery-order-price?venue_slug=my_venue&cart_value=2000&user_lat=52.5200&user_lon=13.4050


## Sample Response:

{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 0
  }
}


License
MIT License
Feel free to modify and distribute this project as needed.


Contributing
Fork the repo on GitHub.
Create a new branch for your feature or bugfix.
Submit a pull request once your changes are tested and stable.


