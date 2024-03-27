from celery import shared_task, group, chain, chord
from dashboard_etl.extract.progress import ETLProgress
from dashboard_etl.models import Gender, ConfirmationType, HealthFacility, LegalForm, Location, ICD, PayerType
from insuree.models import Gender as srcGender, ConfirmationType as srcConfirmationType
from location.models import HealthFacility as srcHealthFacility, HealthFacilityLegalForm as srcLegalForms, Location as srcLocation
from medical.models import Diagnosis
from payer.models import PayerType as srcPayerType

DATABASE = "dashboard_db"


@shared_task
def run_etl():

    task_group = group(
        extract_gender.s(),
        extract_confirmation_types.s(),
        extract_legal_forms.s(),
        extract_payer_types.s(),
        extract_icd.s(),
        extract_locations.s()
    )

    result = task_group.apply_async(chord=extract_health_facilities.si())
    return result


@shared_task(name="etl_gender")
def extract_gender():
    progress = ETLProgress("gender")
    progress.update_stage("Extracting...")
    src_gender = srcGender.objects.all()

    progress.update_stage("Transferring...")
    existing_gender = set(Gender.objects.using(DATABASE).values_list("code", flat=True))

    progress.update_stage("Loading...")
    for gender in src_gender:
        if gender.code not in existing_gender:
            Gender.objects.using(DATABASE).create(code=gender.code, gender=gender.gender)
    progress.update_stage("Done!")


@shared_task(name="etl_confirmation_type")
def extract_confirmation_types():
    progress = ETLProgress("confirmation_type")

    progress.update_stage("Extracting...")
    src_confirmation_types = srcConfirmationType.objects.all()

    progress.update_stage("Transferring...")
    existing_confirmation_types = set(ConfirmationType.objects.using(DATABASE).values_list("code", flat=True))

    progress.update_stage("Loading...")
    for confirmation_type in src_confirmation_types:
        if confirmation_type.code not in existing_confirmation_types:
            ConfirmationType.objects.using(DATABASE).create(
                code=confirmation_type.code, confirmation_type=confirmation_type.confirmationtype)

    progress.update_stage("Done!")


@shared_task(name="etl_legal_forms")
def extract_legal_forms():
    progress = ETLProgress("legal_forms")

    progress.update_stage("Extracting...")
    src_legal_forms = srcLegalForms.objects.all()

    progress.update_stage("Transferring...")
    existing_legal_forms = LegalForm.objects.using(DATABASE).values_list("code", flat=True)

    progress.update_stage("Loading...")
    for form in src_legal_forms:
        if form.code not in existing_legal_forms:
            LegalForm.objects.using(DATABASE).create(code=form.code, legal_form=form.legal_form)

    progress.update_stage("Done!")


@shared_task(name="etl_payer_types")
def extract_payer_types():
    progress = ETLProgress("payer_types")

    progress.update_stage("Extracting...")
    src_payer_types = srcPayerType.objects.all()

    progress.update_stage("Transferring...")
    existing_payer_types = PayerType.objects.using(DATABASE).values_list("code", flat=True)

    progress.update_stage("Loading...")
    for payer_type in src_payer_types:
        if payer_type.code not in existing_payer_types:
            PayerType.objects.using(DATABASE).create(code=payer_type.code, payer_type=payer_type.payer_type)

    progress.update_stage("Done!")


@shared_task(name="etl_icd")
def extract_icd():
    progress = ETLProgress("icd")

    progress.update_stage("Extracting...")
    src_icd = Diagnosis.objects.filter(validity_to__isnull=True)

    progress.update_stage("Transferring...")
    existing_icd = set(ICD.objects.using(DATABASE).values_list("id", flat=True))
    icd_to_create = [icd for icd in src_icd if icd.id not in existing_icd]

    progress.update_stage("Loading...")
    data_list = []
    for icd in icd_to_create:
        if icd.id not in existing_icd:
            data_list.append(ICD(id=icd.id, code=icd.code, name=icd.name))

    ICD.objects.using(DATABASE).bulk_create(data_list)

    progress.update_stage("Done!")


@shared_task(name="etl_locations")
def extract_locations():
    progress = ETLProgress("locations")

    progress.update_stage("Extracting...")
    src_locations = srcLocation.objects.filter(
        validity_to__isnull=True).select_related("parent").order_by("id")

    progress.update_stage("Transferring...")
    existing_locations = set(Location.objects.using(DATABASE).values_list("id", flat=True))
    locations_to_create = [loc for loc in src_locations if loc.id not in existing_locations]

    progress.update_stage("Loading...")
    data_list = []
    for location in locations_to_create:
        data_list.append(Location(id=location.id,
                                  code=location.code,
                                  name=location.name,
                                  male_population=location.male_population,
                                  female_population=location.female_population,
                                  other_population=location.other_population,
                                  households=location.families,
                                  parent_id=location.parent.id if location.parent else None))

    Location.objects.using(DATABASE).bulk_create(data_list)

    progress.update_stage("Done!")


@shared_task(name="etl_health_facilities")
def extract_health_facilities():
    progress = ETLProgress("health_facilities")

    progress.update_stage("Extracting...")
    src_health_facilities = srcHealthFacility.objects.filter(
        validity_to__isnull=True, location__validity_to__isnull=True).select_related("legal_form").select_related("location")

    progress.update_stage("Transferring...")
    existing_health_facilities = set(HealthFacility.objects.using(DATABASE).values_list("id", flat=True))

    health_facilities_to_create = [hf for hf in src_health_facilities if hf.id not in existing_health_facilities]
    legal_forms = LegalForm.objects.using(DATABASE).all()

    progress.update_stage("Loading...")
    data_list = []
    for health_facility in health_facilities_to_create:
        data_list.append(HealthFacility(id=health_facility.id,
                                        code=health_facility.code,
                                        name=health_facility.name,
                                        level=health_facility.level,
                                        legal_form=legal_forms.get(code=health_facility.legal_form.code),
                                        location_id=health_facility.location.id))

    HealthFacility.objects.using(DATABASE).bulk_create(data_list)

    progress.update_stage("Done!")
