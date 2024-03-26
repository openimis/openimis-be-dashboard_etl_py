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
INDICATOR = "visit_by_insurees"


@shared_task
def run_etl():
    try:
        instance = VisitByInsureeExtractor()
        extracted_data = instance.extract()
        transformed_data = instance.transform(extracted_data)
        instance.load(transformed_data)
    except Exception as ex:
        print(ex)
        instance.progress_tracker.update_stage("ERROR!")


class VisitByInsureeExtractor(ETLBase):

    def __init__(self) -> None:
        self.progress_tracker = ETLProgress(INDICATOR)
        self.engine_src = create_engine(source_con_str)
        self.engine_dest = create_engine(dest_con_str, fast_executemany=True)

    def execute_sql(self, sql, engine):
        with engine.connect() as conn:
            result = conn.execute(sql)
            return result.mappings().all()

    def get_max_last_id(self):
        sql = text("SELECT ISNULL(MAX(LastId), 0) LastId FROM VisitByInsurees")
        max_id = self.execute_sql(sql, self.engine_dest)
        return max_id[0]["LastId"]

    def extract(self):
        self.progress_tracker.update_stage("Extracting...")
        max_id = self.get_max_last_id()

        sql = text(f"""
                    SELECT COUNT(1) TotalVisit,ISNULL(C.DateTo, C.DateFrom) Period, I.Gender, DATEDIFF(DAY, I.DOB, ISNULL(C.DateTo, C.DateFrom))/365 Age, F.LocationId, C.HFID, F.ConfirmationType, 
                    (SELECT MAX(ClaimId) FROM tblClaim WHERE ValidityTo IS NULL) LastId
                    FROM tblClaim C
                    INNER JOIN tblInsuree I ON I.InsureeId = C.InsureeID
                    INNER JOIN tblGender G ON G.Code = I.Gender
                    INNER JOIN tblFamilies F ON F.FamilyId = I.FamilyID
                    INNER JOIN tblHF HF ON HF.HFID = C.HFID
                    INNER JOIN tblLocations L ON L.LocationId = HF.LocationId
                    WHERE C.ValidityTo IS NULL
                    AND F.ValidityTo IS NULL
                    AND HF.ValidityTo IS NULL
                    AND L.ValidityTo IS NULL
                    GROUP BY I.Gender, ISNULL(C.DateTo, C.DateFrom), DATEDIFF(DAY, I.DOB, ISNULL(C.DateTo, C.DateFrom))/365, F.LocationId, C.HFID, F.ConfirmationType

""")
        return self.execute_sql(sql, self.engine_src)


    def transform(self, data):
        self.progress_tracker.update_stage("Transforming...")
        transformed_data = []
        for row in data:
            transformed_data.append({
                "total_visit": row["TotalVisit"],
                "period": row["Period"],
                "gender": row["Gender"],
                "age": row["Age"],
                "location_id": row["LocationId"],
                "hf_id": row["HFID"],
                "confirmation_type": row["ConfirmationType"] if row["ConfirmationType"] else None,
                "last_id": row["LastId"]
            })

        return transformed_data


    def load(self, data):
        self.progress_tracker.update_stage("Loading...")
        sql = text("""
                    INSERT INTO VisitByInsurees (TotalVisit, Period, Gender, Age, LocationId, HFID, ConfirmationType, LastId)
                    VALUES(:total_visit, :period, :gender, :age, :location_id, :hf_id, :confirmation_type, :last_id)
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
