from django.urls import path
from .views import extract_base_data

urlpatterns = [
    path("extract_base_data", extract_base_data, name="extract_base_data")
]
