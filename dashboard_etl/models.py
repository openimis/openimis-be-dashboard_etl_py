from django.db import models


class AgeGroup(models.Model):
    min_age = models.IntegerField(db_column="MinAge")
    max_age = models.IntegerField(db_column="MaxAge")
    age_group = models.CharField(db_column="AgeGroup", max_length=20)


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
    parent_id = models.ForeignKey('self', db_column="ParentLocationId",
                                  on_delete=models.SET_NULL, related_name="children")
    male_population = models.IntegerField(db_column="MalePopulation")
    female_population = models.IntegerField(db_column="FemalePopulation")
    other_population = models.IntegerField(db_column="OtherPopulation")
    households = models.IntegerField(db_column="Households")

    class Meta:
        db_table = "Locations"


class HealthFacility(models.Model):
    id = models.IntegerField(db_column="HFID", primary_key=True)
    code = models.CharField(db_column="HFCode", max_length=8)
    name = models.CharField(db_column="HFName", max_length=100)
    legal_form = models.ForeignKey(LegalForm, db_column="LegalForm", max_length=1,
                                   on_delete=models.SET_NULL, related_name="helath_facilities")
    level = models.CharField(db_column="HFLevel", max_length=1)
    location = models.ForeignKey(Location, db_column="LocationId",
                                 on_delete=models.SET_NULL, related_name="helath_facilities")

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
    location = models.ForeignKey(Location, db_column="LocationId",
                                 on_delete=models.SET_NULL, related_name="active_households")
    gender = models.ForeignKey(Gender, db_column="Gender",
                               on_delete=models.SET_NULL, related_name="active_households")
    age = models.IntegerField(db_column="Age")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType",
                                          on_delete=models.SET_NULL, related_name="active_households")
    benefit_amount = models.DecimalField(db_column="BenefitAmount")

    class Meta:
        db_table = "ActiveHouseholds"


class InsuredHousehold(models.Model):
    insured_households = models.IntegerField(db_column="InsuredHouseholds")
    period = models.DateField(db_column="InsuredDate")
    location = models.ForeignKey(Location, db_column="LocationId",
                                 on_delete=models.SET_NULL, related_name="insured_households")
    gender = models.ForeignKey(Gender, db_column="Gender",
                               on_delete=models.SET_NULL, related_name="insured_households")
    age = models.IntegerField(db_column="Age")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType",
                                          on_delete=models.SET_NULL, related_name="insured_households")
    policy_stage = models.CharField(db_column="PolicyStage", max_length=1)


    class Meta:
        db_table = "InsuredHouseholds"


class ActiveInsuree(models.Model):
    active_insurees = models.IntegerField(db_column="ActiveInsurees")
    period = models.DateField(db_column="ActivePeriod")
    location = models.ForeignKey(Location, db_column="LocationId",
                                 on_delete=models.SET_NULL, related_name="active_insurees")
    gender = models.ForeignKey(Gender, db_column="Gender",
                               on_delete=models.SET_NULL, related_name="active_insurees")
    age = models.IntegerField(db_column="Age")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType",
                                          on_delete=models.SET_NULL, related_name="active_insurees")


    class Meta:
        db_table = "ActiveInsurees"


class InsuredInsuree(models.Model):
    insured_insurees = models.IntegerField(db_column="InsuredInsurees")
    period = models.DateField(db_column="InsuredDate")
    location = models.ForeignKey(Location, db_column="LocationId",
                                 on_delete=models.SET_NULL, related_name="insured_insurees")
    gender = models.ForeignKey(Gender, db_column="Gender",
                               on_delete=models.SET_NULL, related_name="insured_insurees")
    age = models.IntegerField(db_column="Age")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType",
                                          on_delete=models.SET_NULL, related_name="insured_insurees")
    policy_stage = models.CharField(db_column="PolicyStage", max_length=1)


    class Meta:
        db_table = "InsuredInsurees"


class ClaimReceived(models.Model):
    claims_received = models.IntegerField(db_column="ClaimReceived")
    amount = models.DecimalField(db_column="Amount")
    approved = models.DecimalField(db_column="Approved")
    received_date = models.DateField(db_column="ReceivedDate")
    health_facility = models.ForeignKey(HealthFacility, db_column="HFId",
                                        on_delete=models.SET_NULL, related_name="claims")
    age = models.IntegerField(db_column="Age")
    gender = models.ForeignKey(Gender, db_column="Gender",
                               on_delete=models.SET_NULL, related_name="claims")
    location = models.ForeignKey(Location, db_column="LocationId",
                                 on_delete=models.SET_NULL, related_name="claims")
    care_type = models.CharField(db_column="CareType", max_length=4)
    visit_type = models.CharField(db_column="VisitType", max_length=1)
    icd = models.ForeignKey(ICD, db_column="ICDID",
                            on_delete=models.SET_NULL, related_name="claims")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType",
                                          on_delete=models.SET_NULL, related_name="claims")
    processing_days = models.IntegerField(db_column="ProcessingDays")
    claim_status = models.IntegerField(db_column="ClaimStatus")
    review_status = models.IntegerField(db_column="ReviewStatus")
    hf_days = models.IntegerField(db_column="DaysInHF")

    class Meta:
        db_table = "ClaimReceived"


class PremiumCollected(models.Model):
    amount = models.DecimalField(db_column="Amount")
    pay_date = models.DateField(db_column="PayDate")
    pay_type = models.CharField(db_column="PayType", max_length=1)
    location = models.ForeignKey(Location, db_column="LocationId",
                                 on_delete=models.SET_NULL, related_name="premiums")
    payer_type = models.ForeignKey(PayerType, db_column="PayerTypeCode", max_length=1,
                                   on_delete=models.SET_NULL, related_name="premiums")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType",
                                          on_delete=models.SET_NULL, related_name="premiums")
    policy_stage = models.CharField(db_column="PolicyStage", max_length=1)


    class Meta:
        db_table = "PremiumCollected"


class VisitsByInsuree(models.Model):
    visits = models.IntegerField(db_column="TotalVisit")
    period = models.DateField(db_column="InsuredDate")
    gender = models.ForeignKey(Gender, db_column="Gender",
                               on_delete=models.SET_NULL, related_name="visits")
    age = models.IntegerField(db_column="Age")
    location = models.ForeignKey(Location, db_column="LocationId",
                                 on_delete=models.SET_NULL, related_name="visits")
    health_facility = models.ForeignKey(HealthFacility, db_column="HFId",
                                        on_delete=models.SET_NULL, related_name="visits")
    confirmation_type = models.ForeignKey(ConfirmationType, db_column="ConfirmationType",
                                          on_delete=models.SET_NULL, related_name="visits")


    class Meta:
        db_table = "VisitByInsurees"
