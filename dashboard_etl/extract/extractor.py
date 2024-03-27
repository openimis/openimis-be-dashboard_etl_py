from celery import shared_task, group
from .base_data_extract import run_etl as base_data_etl
from .extract_activehouseholds import run_etl as active_households_etl
from .extract_active_insurees import run_etl as active_insurees_etl
from .extract_claim_received import run_etl as claims_etl
from .extract_insured_households import run_etl as insured_households_etl
from .extract_insured_insurees import run_etl as insured_insurees_etl
from .extract_premium_collected import run_etl as premium_collected_etl
from .extract_visit_by_insuree import run_etl as visits_etl


@shared_task
def run_base_data_etl():
    return base_data_etl()


@shared_task
def run_indicators_etl():
    task_group = group(
        active_households_etl.s(),
        active_insurees_etl.s(),
        claims_etl.s(),
        insured_households_etl.s(),
        insured_insurees_etl.s(),
        premium_collected_etl.s(),
        visits_etl.s()
    )
    return task_group()