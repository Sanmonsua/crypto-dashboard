from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('search', search_coins),
    path('load_coins', load_coins)
]
