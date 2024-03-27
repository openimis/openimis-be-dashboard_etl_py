from django.urls import path
from .views import etl, get_task_progress

urlpatterns = [
    path("etl", etl, name="etl"),
    path("get_task_progress", get_task_progress, name="get_task_progress")
]
