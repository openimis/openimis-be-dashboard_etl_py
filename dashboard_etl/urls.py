from django.urls import path
from .views import extract_base_data, extract_indicators

urlpatterns = [
    path("extract_base_data", extract_base_data, name="extract_base_data"),
    path("extract_indicators", extract_indicators, name="extract_indicators")
]
