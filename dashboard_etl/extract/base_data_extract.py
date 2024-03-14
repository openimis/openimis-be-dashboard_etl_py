from dashboard_etl.models import Gender, ConfirmationType, HealthFacility, LegalForm, Location, ICD, PayerType
from insuree.models import Gender as srcGender, ConfirmationType as srcConfirmationType
from location.models import HealthFacility as srcHealthFacility, HealthFacilityLegalForm as srcLegalForms, Location as srcLocation
from medical.models import Diagnosis
from payer.models import PayerType as srcPayerType

DATABASE = "dashboard_db"


class BaseExtractor:

    def extract_base_data(self):
        self.extract_gender()
        self.extract_confirmation_types()
        self.extract_health_facilities()
        self.extract_legal_forms()
        self.extract_payer_types()
        self.extract_icd()
        self.extract_locations()
        self.extract_health_facilities()

    def extract_gender(self):
        src_gender = srcGender.objects.all()
        existing_gender = set(Gender.objects.using(DATABASE).values_list("code", flat=True))
        for gender in src_gender:
            if gender.code not in existing_gender:
                Gender.objects.using(DATABASE).create(code=gender.code, gender=gender.gender)
        print("Gender extracted...")

    def extract_confirmation_types(self):
        src_confirmation_types = srcConfirmationType.objects.all()
        existing_confirmation_types = set(ConfirmationType.objects.using(DATABASE).values_list("code", flat=True))

        for confirmation_type in src_confirmation_types:
            if confirmation_type.code not in existing_confirmation_types:
                ConfirmationType.objects.using(DATABASE).create(
                    code=confirmation_type.code, confirmation_type=confirmation_type.confirmationtype)

        print("Confirmation types extracted...")

    def extract_legal_forms(self):
        src_legal_forms = srcLegalForms.objects.all()
        existing_legal_forms = LegalForm.objects.using(DATABASE).values_list("code", flat=True)

        for form in src_legal_forms:
            if form.code not in existing_legal_forms:
                LegalForm.objects.using(DATABASE).create(code=form.code, legal_form=form.legal_form)

        print("Legal forms extracted...")

    def extract_payer_types(self):
        src_payer_types = srcPayerType.objects.all()
        existing_payer_types = PayerType.objects.using(DATABASE).values_list("code", flat=True)

        for payer_type in src_payer_types:
            if payer_type.code not in existing_payer_types:
                PayerType.objects.using(DATABASE).create(code=payer_type.code, payer_type=payer_type.payer_type)

        print("payer types extracted...")


    def extract_icd(self):
        src_icd = Diagnosis.objects.filter(validity_to__isnull=True)
        existing_icd = set(ICD.objects.using(DATABASE).values_list("id", flat=True))
        icd_to_create = [icd for icd in src_icd if icd.id not in existing_icd]
        data_list = []
        for icd in icd_to_create:
            if icd.id not in existing_icd:
                data_list.append(ICD(id=icd.id, code=icd.code, name=icd.name))

        ICD.objects.using(DATABASE).bulk_create(data_list)

        print("ICD Codes exported...")


    def extract_locations(self):
        src_locations = srcLocation.objects.filter(
            validity_to__isnull=True).select_related("parent").order_by("id")
        existing_locations = set(Location.objects.using(DATABASE).values_list("id", flat=True))
        locations_to_create = [loc for loc in src_locations if loc.id not in existing_locations]

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

        print("Locations extracted...")

    def extract_health_facilities(self):
        src_health_facilities = srcHealthFacility.objects.filter(
            validity_to__isnull=True, location__validity_to__isnull=True).select_related("legal_form").select_related("location")
        existing_health_facilities = set(HealthFacility.objects.using(DATABASE).values_list("id", flat=True))

        health_facilities_to_create = [hf for hf in src_health_facilities if hf.id not in existing_health_facilities]
        legal_forms = LegalForm.objects.using(DATABASE).all()

        data_list = []
        for health_facility in health_facilities_to_create:
            data_list.append(HealthFacility(id=health_facility.id,
                                            code=health_facility.code,
                                            name=health_facility.name,
                                            level=health_facility.level,
                                            legal_form=legal_forms.get(code=health_facility.legal_form.code),
                                            location_id=health_facility.location.id))

        HealthFacility.objects.using(DATABASE).bulk_create(data_list)

        print("Health facilities extracted...")
