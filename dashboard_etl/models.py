from django.db import models


class AgeGroup(models.Model):
    min_age = models.IntegerField(db_column="MinAge")
    max_age = models.IntegerField(db_column="MaxAge")
    age_group = models.CharField(db_column="AgeGroup", max_length=20)

    class Meta:
        db_table = "AgeGroup"


class ConfirmationType(models.Model):
    code = models.CharField(db_column="Code", max_length=3, primary_key=True)
    confirmation_type = models.CharField(db_column="ConfirmationType", max_length=50)

    class Meta:
        db_table = "ConfirmationTypes"


class Gender(models.Model):
    code = models.CharField(db_column="Code", max_length=1, primary_key=True)
    gender = models.CharField(db_column="Gender", max_length=50)

    class Meta:
        db_table = "Gender"


class LegalForm(models.Model):
    code = models.CharField(db_column="LegalFormCode", max_length=1, primary_key=True)
    legal_form = models.CharField(db_column="LegalForms", max_length=50)

    class Meta:
        db_table = "LegalForms"


class Location(models.Model):
    id = models.IntegerField(db_column="LocationId", primary_key=True)
    code = models.CharField(db_column="LocationCode", max_length=8)
    name = models.CharField(db_column="LocationName", max_length=50)
    parent = models.ForeignKey('self', db_column="ParentLocationId", null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="children")
    male_population = models.IntegerField(db_column="MalePopulation", null=True, blank=True)
    female_population = models.IntegerField(db_column="FemalePopulation", null=True, blank=True)
    other_population = models.IntegerField(db_column="OtherPopulation", null=True, blank=True)
    households = models.IntegerField(db_column="Households", null=True, blank=True)

    class Meta:
        db_table = "Locations"


class HealthFacility(models.Model):
    id = models.IntegerField(db_column="HFID", primary_key=True)
    code = models.CharField(db_column="HFCode", max_length=8)
    name = models.CharField(db_column="HFName", max_length=100)
    legal_form = models.ForeignKey(LegalForm, db_column="LegalForm", max_length=1, null=True,
                                   on_delete=models.SET_NULL, related_name="health_facilities")
    level = models.CharField(db_column="HFLevel", max_length=1)
    location = models.ForeignKey(Location, db_column="LocationId", null=True,
                                 on_delete=models.SET_NULL, related_name="health_facilities")

    class Meta:
        db_table = "HealthFacilities"


class ICD(models.Model):
    id = models.IntegerField(db_column="ICDID", primary_key=True)
    code = models.CharField(db_column="ICDCode", max_length=6)
    name = models.CharField(db_column="ICDName", max_length=255)

    class Meta:
        db_table = "ICDCodes"


class PayerType(models.Model):
    code = models.CharField(db_column="Code", max_length=1, primary_key=True)
    payer_type = models.CharField(db_column="PayerType", max_length=50)

    class Meta:
        db_table = "PayerType"


class ActiveHousehold(models.Model):
    active_households = models.IntegerField(db_column="ActiveHouseholds")
    period = models.DateField(db_column="ActivePeriod")
    location = models.ForeignKey(Location, db_column="LocationId", null=True,
                                 on_delete=models.SET_NULL, related_name="active_households")
    gender = models.ForeignKey(Gender, db_column="Gender", null=True,
                               on_delete=models.SET_NULL, related_name="active_households")
    age = models.IntegerField(db_column="Age")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType", null=True,
                                          on_delete=models.SET_NULL, related_name="active_households")
    benefit_amount = models.DecimalField(db_column="BenefitAmount", decimal_places=2, max_digits=18)
    last_id = models.IntegerField(db_column="LastId")

    class Meta:
        db_table = "ActiveHouseholds"


class InsuredHousehold(models.Model):
    insured_households = models.IntegerField(db_column="InsuredHouseholds")
    period = models.DateField(db_column="InsuredDate")
    location = models.ForeignKey(Location, db_column="LocationId", null=True,
                                 on_delete=models.SET_NULL, related_name="insured_households")
    gender = models.ForeignKey(Gender, db_column="Gender", null=True,
                               on_delete=models.SET_NULL, related_name="insured_households")
    age = models.IntegerField(db_column="Age", null=True)
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType", null=True,
                                          on_delete=models.SET_NULL, related_name="insured_households")
    policy_stage = models.CharField(db_column="PolicyStage", max_length=1, null=True)
    last_id = models.IntegerField(db_column="LastId")


    class Meta:
        db_table = "InsuredHouseholds"


class ActiveInsuree(models.Model):
    active_insurees = models.IntegerField(db_column="ActiveInsurees")
    period = models.DateField(db_column="ActivePeriod")
    location = models.ForeignKey(Location, db_column="LocationId", null=True,
                                 on_delete=models.SET_NULL, related_name="active_insurees")
    gender = models.ForeignKey(Gender, db_column="Gender", null=True,
                               on_delete=models.SET_NULL, related_name="active_insurees")
    age = models.IntegerField(db_column="Age")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType", null=True,
                                          on_delete=models.SET_NULL, related_name="active_insurees")
    last_id = models.IntegerField(db_column="LastId")

    class Meta:
        db_table = "ActiveInsurees"


class InsuredInsuree(models.Model):
    insured_insurees = models.IntegerField(db_column="InsuredInsurees")
    period = models.DateField(db_column="InsuredDate")
    location = models.ForeignKey(Location, db_column="LocationId", null=True,
                                 on_delete=models.SET_NULL, related_name="insured_insurees")
    gender = models.ForeignKey(Gender, db_column="Gender", null=True,
                               on_delete=models.SET_NULL, related_name="insured_insurees")
    age = models.IntegerField(db_column="Age")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType", null=True,
                                          on_delete=models.SET_NULL, related_name="insured_insurees")
    policy_stage = models.CharField(db_column="PolicyStage", max_length=1, null=True)
    last_id = models.IntegerField(db_column="LastId")

    class Meta:
        db_table = "InsuredInsurees"


class ClaimReceived(models.Model):
    claims_received = models.IntegerField(db_column="ClaimReceived")
    amount = models.DecimalField(db_column="Amount", decimal_places=2, max_digits=18, null=True, blank=True)
    approved = models.DecimalField(db_column="Approved", decimal_places=2, max_digits=18, null=True, blank=True)
    received_date = models.DateField(db_column="ReceivedDate")
    health_facility = models.ForeignKey(HealthFacility, db_column="HFId", null=True,
                                        on_delete=models.SET_NULL, related_name="claims")
    age = models.IntegerField(db_column="Age", null=True, blank=True)
    gender = models.ForeignKey(Gender, db_column="Gender", null=True,
                               on_delete=models.SET_NULL, related_name="claims")
    location = models.ForeignKey(Location, db_column="LocationId", null=True,
                                 on_delete=models.SET_NULL, related_name="claims")
    care_type = models.CharField(db_column="CareType", max_length=4, null=True, blank=True)
    visit_type = models.CharField(db_column="VisitType", max_length=1, null=True, blank=True)
    icd = models.ForeignKey(ICD, db_column="ICDID", null=True,
                            on_delete=models.SET_NULL, related_name="claims")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType", null=True,
                                          on_delete=models.SET_NULL, related_name="claims")
    processing_days = models.IntegerField(db_column="ProcessingDays", null=True, blank=True)
    claim_status = models.IntegerField(db_column="ClaimStatus", null=True, blank=True)
    review_status = models.IntegerField(db_column="ReviewStatus", null=True, blank=True)
    hf_days = models.IntegerField(db_column="DaysInHF", null=True, blank=True)
    last_id = models.IntegerField(db_column="LastId", null=True, blank=True)

    class Meta:
        db_table = "ClaimReceived"


class PremiumCollected(models.Model):
    amount = models.DecimalField(db_column="Amount", decimal_places=2, max_digits=18, null=True)
    pay_date = models.DateField(db_column="PayDate")
    pay_type = models.CharField(db_column="PayType", max_length=1, null=True)
    location = models.ForeignKey(Location, db_column="LocationId", null=True,
                                 on_delete=models.SET_NULL, related_name="premiums")
    payer_type = models.ForeignKey(PayerType, db_column="PayerTypeCode", max_length=1, null=True,
                                   on_delete=models.SET_NULL, related_name="premiums")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType", null=True,
                                          on_delete=models.SET_NULL, related_name="premiums")
    policy_stage = models.CharField(db_column="PolicyStage", max_length=1, null=True)
    last_id = models.IntegerField(db_column="LastId", null=True, blank=True)



    class Meta:
        db_table = "PremiumCollected"


class VisitsByInsuree(models.Model):
    visits = models.IntegerField(db_column="TotalVisit")
    period = models.DateField(db_column="InsuredDate")
    gender = models.ForeignKey(Gender, db_column="Gender", null=True,
                               on_delete=models.SET_NULL, related_name="visits")
    age = models.IntegerField(db_column="Age")
    location = models.ForeignKey(Location, db_column="LocationId", null=True,
                                 on_delete=models.SET_NULL, related_name="visits")
    health_facility = models.ForeignKey(HealthFacility, db_column="HFId", null=True,
                                        on_delete=models.SET_NULL, related_name="visits")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType", null=True,
                                          on_delete=models.SET_NULL, related_name="visits")


    class Meta:
        db_table = "VisitByInsurees"
