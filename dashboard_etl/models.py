from django.db import models


class AgeGroup(models.Model):
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    age_group = models.CharField(max_length=20)

    class Meta:
        db_table = "age_groups"


class ConfirmationType(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    confirmation_type = models.CharField(max_length=50)

    class Meta:
        db_table = "confirmation_types"


class Gender(models.Model):
    code = models.CharField(max_length=1, primary_key=True)
    gender = models.CharField(max_length=50)

    class Meta:
        db_table = "genders"


class LegalForm(models.Model):
    code = models.CharField(max_length=1, primary_key=True)
    legal_form = models.CharField(max_length=50)

    class Meta:
        db_table = "legal_forms"


class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="children")
    male_population = models.IntegerField(null=True, blank=True)
    female_population = models.IntegerField(null=True, blank=True)
    other_population = models.IntegerField(null=True, blank=True)
    households = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "locations"


class HealthFacility(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    legal_form = models.ForeignKey(LegalForm, db_column="legal_form", max_length=1, null=True,
                                   on_delete=models.SET_NULL, related_name="health_facilities")
    level = models.CharField(max_length=1)
    location = models.ForeignKey(Location, null=True,
                                 on_delete=models.SET_NULL, related_name="health_facilities")

    class Meta:
        db_table = "health_facilities"


class ICD(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "icd"


class PayerType(models.Model):
    code = models.CharField(max_length=1, primary_key=True)
    payer_type = models.CharField(max_length=50)

    class Meta:
        db_table = "payer_types"


class ActiveHousehold(models.Model):
    active_households = models.IntegerField()
    period = models.DateField()
    location = models.ForeignKey(Location, null=True,
                                 on_delete=models.SET_NULL, related_name="active_households")
    gender = models.ForeignKey(Gender, db_column="gender", null=True,
                               on_delete=models.SET_NULL, related_name="active_households")
    age = models.IntegerField()
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="confirmation_type", null=True,
                                          on_delete=models.SET_NULL, related_name="active_households")
    benefit_amount = models.DecimalField(decimal_places=2, max_digits=18)
    last_id = models.IntegerField()

    class Meta:
        db_table = "active_households"


class InsuredHousehold(models.Model):
    insured_households = models.IntegerField()
    period = models.DateField()
    location = models.ForeignKey(Location, null=True,
                                 on_delete=models.SET_NULL, related_name="insured_households")
    gender = models.ForeignKey(Gender, db_column="gender", null=True,
                               on_delete=models.SET_NULL, related_name="insured_households")
    age = models.IntegerField(null=True)
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="confirmation_type", null=True,
                                          on_delete=models.SET_NULL, related_name="insured_households")
    policy_stage = models.CharField(max_length=1, null=True)
    last_id = models.IntegerField()


    class Meta:
        db_table = "insured_households"


class ActiveInsuree(models.Model):
    active_insurees = models.IntegerField()
    period = models.DateField()
    location = models.ForeignKey(Location, null=True,
                                 on_delete=models.SET_NULL, related_name="active_insurees")
    gender = models.ForeignKey(Gender, db_column="gender", null=True,
                               on_delete=models.SET_NULL, related_name="active_insurees")
    age = models.IntegerField()
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="confirmation_type", null=True,
                                          on_delete=models.SET_NULL, related_name="active_insurees")
    last_id = models.IntegerField()

    class Meta:
        db_table = "active_insurees"


class InsuredInsuree(models.Model):
    insured_insurees = models.IntegerField()
    period = models.DateField()
    location = models.ForeignKey(Location, null=True,
                                 on_delete=models.SET_NULL, related_name="insured_insurees")
    gender = models.ForeignKey(Gender, db_column="gender", null=True,
                               on_delete=models.SET_NULL, related_name="insured_insurees")
    age = models.IntegerField()
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="confirmation_type", null=True,
                                          on_delete=models.SET_NULL, related_name="insured_insurees")
    policy_stage = models.CharField(max_length=1, null=True)
    last_id = models.IntegerField()

    class Meta:
        db_table = "insured_insurees"


class ClaimReceived(models.Model):
    claims_received = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=18, null=True, blank=True)
    approved = models.DecimalField(decimal_places=2, max_digits=18, null=True, blank=True)
    received_date = models.DateField()
    health_facility = models.ForeignKey(HealthFacility, null=True,
                                        on_delete=models.SET_NULL, related_name="claims")
    age = models.IntegerField(null=True, blank=True)
    gender = models.ForeignKey(Gender, db_column="gender", null=True,
                               on_delete=models.SET_NULL, related_name="claims")
    location = models.ForeignKey(Location, null=True,
                                 on_delete=models.SET_NULL, related_name="claims")
    care_type = models.CharField(max_length=4, null=True, blank=True)
    visit_type = models.CharField(max_length=1, null=True, blank=True)
    icd = models.ForeignKey(ICD, null=True,
                            on_delete=models.SET_NULL, related_name="claims")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="confirmation_type", null=True,
                                          on_delete=models.SET_NULL, related_name="claims")
    processing_days = models.IntegerField(null=True, blank=True)
    claim_status = models.IntegerField(null=True, blank=True)
    review_status = models.IntegerField(null=True, blank=True)
    hf_days = models.IntegerField(null=True, blank=True)
    last_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "claims"


class PremiumCollected(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=18, null=True)
    pay_date = models.DateField()
    pay_type = models.CharField(max_length=1, null=True)
    location = models.ForeignKey(Location, null=True,
                                 on_delete=models.SET_NULL, related_name="premiums")
    payer_type = models.ForeignKey(PayerType, db_column="payer_type", max_length=1, null=True,
                                   on_delete=models.SET_NULL, related_name="premiums")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="confirmation_type", null=True,
                                          on_delete=models.SET_NULL, related_name="premiums")
    policy_stage = models.CharField(max_length=1, null=True)
    last_id = models.IntegerField(null=True, blank=True)



    class Meta:
        db_table = "premiums"


class VisitsByInsuree(models.Model):
    visits = models.IntegerField()
    period = models.DateField(null=True)
    gender = models.ForeignKey(Gender, db_column="gender", null=True,
                               on_delete=models.SET_NULL, related_name="visits")
    age = models.IntegerField(null=True)
    location = models.ForeignKey(Location, null=True,
                                 on_delete=models.SET_NULL, related_name="visits")
    health_facility = models.ForeignKey(HealthFacility, null=True,
                                        on_delete=models.SET_NULL, related_name="visits")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="confirmation_type", null=True,
                                          on_delete=models.SET_NULL, related_name="visits")
    last_id = models.IntegerField(null=True, blank=True)


    class Meta:
        db_table = "visits"
