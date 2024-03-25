from celery import shared_task, group
from .extract_activehouseholds import run_etl as active_households_etl
from .extract_active_insurees import run_etl as active_insruees_etl
from .extract_claim_received import run_etl as claims_etl


@shared_task
def run_etl():
    task_group = group(
        # active_households_etl(),
        # active_insruees_etl(),
        claims_etl()
    )
    return task_group()
