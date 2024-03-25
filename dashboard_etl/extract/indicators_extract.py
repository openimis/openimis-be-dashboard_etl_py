from celery import shared_task, group
from .extract_activehouseholds import run_etl as active_households_etl
from .extract_active_insurees import run_etl as active_insruees_etl


@shared_task
def run_etl():
    task_group = group(active_households_etl(), active_insruees_etl())
    task_group()
    # active_households_etl.delay()
    # active_insruees_etl.delay()

    # indicators = [
    #     (ActiveHouseholdExtractor, "active_household"),
    #     (ActiveInsureesExtractor, "active_insurees"),
    # ]

    # for class_name, indicator in indicators:
    #     instance = class_name()
    #     instance.run_etl.delay()

    return "ETL Started!!!"
