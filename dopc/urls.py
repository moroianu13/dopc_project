from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/delivery-order-price', views.calculate_price, name='calculate_price'),
]
