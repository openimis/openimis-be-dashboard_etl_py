from django.urls import path
from .views import extract_base_data, extract_indicators, get_task_progress

urlpatterns = [
    path("extract_base_data", extract_base_data, name="extract_base_data"),
    path("extract_indicators", extract_indicators, name="extract_indicators"),
    path("get_task_progress", get_task_progress, name="get_task_progress")
]
