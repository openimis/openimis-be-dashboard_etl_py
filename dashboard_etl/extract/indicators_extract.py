import asyncio
from asgiref.sync import async_to_sync
from celery import shared_task
from .extract_activehouseholds import ActiveHouseholdExtractor


@shared_task
def run_etl():
    indicators = [
        (ActiveHouseholdExtractor, "active_household"),
    ]

    for class_name, indicator in indicators:
        # yield f"{indicator} ETL Started"
        isinstance = class_name()
        return isinstance.run_etl()
    # return "ETL Started!!!"
