from decimal import Decimal
from dashboard_etl.extract.progress import ETLProgress
from django.apps import apps
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from .etl_base import ETLBase
from celery import shared_task

BATCH_SIZE = apps.get_app_config("dashboard_etl").batch_size
source_con_str = apps.get_app_config("dashboard_etl").src_con_str
dest_con_str = apps.get_app_config("dashboard_etl").dest_con_str
INDICATOR = "claim_received"


@shared_task(name="etl_claims")
def run_etl():
    try:
        instance = ClaimReceivedExtractor()
        extracted_data = instance.extract()
        transformed_data = instance.transform(extracted_data)
        instance.load(transformed_data)
    except Exception as ex:
        print(ex)
        instance.progress_tracker.update_stage("ERROR!")


class ClaimReceivedExtractor(ETLBase):

    def __init__(self) -> None:
        self.progress_tracker = ETLProgress(INDICATOR)
        self.engine_src = create_engine(source_con_str)
        self.engine_dest = create_engine(dest_con_str, fast_executemany=True)

    def execute_sql(self, sql, engine):
        with engine.connect() as conn:
            result = conn.execute(sql)
            return result.mappings().all()

    def get_max_last_id(self):
        sql = text("SELECT ISNULL(MAX(LastId), 0) LastId FROM ClaimReceived")
        max_id = self.execute_sql(sql, self.engine_dest)
        return max_id[0]["LastId"]

    def extract(self):
        self.progress_tracker.update_stage("Extracting...")
        max_id = self.get_max_last_id()

        sql = text(f"""
                    SELECT COUNT(DISTINCT C.ClaimID)TotalClaimReceived, SUM(C.Claimed)Amount, CASE WHEN C.ClaimStatus >=8 THEN SUM(ISNULL(C.Approved, C.Claimed)) ELSE NULL END Approved, CAST(SubmitStamp AS DATE) SubmitDate, HF.HfID, DATEDIFF(DAY, I.DOB, C.SubmitStamp)/365 Age, I.Gender, F.LocationId, C.CareType, 
                    CASE WHEN C.VisitType IS NULL THEN 'O' ELSE C.VisitType END VisitType, C.ICDID, F.ConfirmationType,DATEDIFF(DAY, C.SubmitStamp, C.ProcessStamp)ProcessingDays, C.ClaimStatus, C.ReviewStatus,
                    DATEDIFF(DAY, C.DateFrom, C.DateTo)DaysInHF, (SELECT MAX(ClaimId) FROM tblClaim WHERE ValidityTo IS NULL) LastId
                    FROM tblClaim C  
                    INNER JOIN tblHF HF ON C.HFID = HF.HFID
                    INNER JOIN tblLocations L ON HF.Locationid = L.LocationId
                    INNER JOIN tblInsuree I ON I.InsureeId = C.InsureeID
                    INNER JOIN tblFamilies F ON F.FamilyId = I.FamilyID
                    WHERE C.ValidityTo IS NULL 
                    AND C.SubmitStamp IS NOT NULL
                    AND HF.ValidityTo IS NULL
                    AND L.ValidityTo IS NULL
                    AND I.ValidityTo IS NULL
                    AND F.ValidityTo IS NULL
                    AND C.ClaimId > {max_id}
                    GROUP BY CAST(SubmitStamp AS DATE), HF.HfID, DATEDIFF(DAY, I.DOB, C.SubmitStamp)/365, I.Gender, F.LocationId, C.CareType, C.VisitType, C.ICDID, F.ConfirmationType, C.SubmitStamp, C.ProcessStamp, C.ClaimStatus, C.ReviewStatus, DATEDIFF(DAY, C.DateFrom, C.DateTo)
           

""")
        return self.execute_sql(sql, self.engine_src)


    def transform(self, data):
        self.progress_tracker.update_stage("Transforming...")
        transformed_data = []
        for row in data:
            transformed_data.append({
                "claims_received": row["TotalClaimReceived"],
                "amount": row["Amount"],
                "approved": row["Approved"],
                "received_date": row["SubmitDate"],
                "health_facility_id": row["HfID"],
                "age": row["Age"],
                "gender": row["Gender"],
                "location_id": row["LocationId"],
                "care_type": row["CareType"],
                "visit_type": row["VisitType"],
                "icd_id": row["ICDID"],
                "confirmation_type": row["ConfirmationType"] if row["ConfirmationType"] else None,
                "processing_days": row["ProcessingDays"],
                "claim_status": row["ClaimStatus"],
                "review_status": row["ReviewStatus"],
                "hf_days": row["DaysInHF"],
                "last_id": row["LastId"]
            })

        return transformed_data


    def load(self, data):
        self.progress_tracker.update_stage("Loading...")
        sql = text("""
                    INSERT INTO ClaimReceived ([ClaimReceived], [Amount], [Approved], [ReceivedDate], [Age], [CareType], [VisitType], [ProcessingDays], [ClaimStatus], [ReviewStatus], [DaysInHF], [ConfirmationType], [Gender], [HFId], [ICDID], [LocationId], [LastId])
                    VALUES(:claims_received, :amount, :approved, :received_date, :age, :care_type, :visit_type, :processing_days, :claim_status, :review_status, :hf_days, :confirmation_type, :gender, :health_facility_id, :icd_id, :location_id, :last_id)
""")

        page = 0
        total_pages = (len(data) + BATCH_SIZE - 1) // BATCH_SIZE

        with self.engine_dest.connect() as conn:
            for i in range(0, len(data), BATCH_SIZE):
                page += 1
                batch = data[i: i + BATCH_SIZE]
                data_to_insert = [{**row} for row in batch]
                conn.execute(sql, data_to_insert)
                print(f"Page {page}/{total_pages}")
                self.progress_tracker.update_stage(
                    f"{(((Decimal(page)/total_pages)) * 100):.2f}% completed ({page}/{total_pages})")

            conn.commit()

        self.progress_tracker.update_stage("Done!")
