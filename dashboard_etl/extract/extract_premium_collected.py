from decimal import Decimal
from ..models import PremiumCollected
from dashboard_etl.extract.progress import ETLProgress
from django.apps import apps
from django.db.models import Max
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from .etl_base import ETLBase
from celery import shared_task

BATCH_SIZE = apps.get_app_config("dashboard_etl").batch_size
source_con_str = apps.get_app_config("dashboard_etl").src_con_str
dest_con_str = apps.get_app_config("dashboard_etl").dest_con_str
INDICATOR = "premium_collected"


@shared_task(name="etl_premium_collected")
def run_etl():
    try:
        instance = PremiumCollectedExtractor()
        extracted_data = instance.extract()
        transformed_data = instance.transform(extracted_data)
        instance.load(transformed_data)
    except Exception as ex:
        print(ex)
        instance.progress_tracker.update_stage("ERROR!")


class PremiumCollectedExtractor(ETLBase):

    def __init__(self) -> None:
        self.progress_tracker = ETLProgress(INDICATOR)
        self.engine_src = create_engine(source_con_str)
        if dest_con_str.startswith("mssql"):
            self.engine_dest = create_engine(dest_con_str, fast_executemany=True)
        else:
            self.engine_dest = create_engine(dest_con_str)

    def execute_sql(self, sql, engine):
        with engine.connect() as conn:
            result = conn.execute(sql)
            return result.mappings().all()

    def get_max_last_id(self):
        return PremiumCollected.objects.using("dashboard_db").aggregate(last_id=Max("last_id"))['last_id'] or 0



    def extract(self):
        self.progress_tracker.update_stage("Extracting...")
        max_id = self.get_max_last_id()

        sql = text(f"""
                    SELECT SUM(PR.Amount) Amount, PR.PayDate, PR.PayType, F.LocationId, PT.Code PayerTypeCode, CT.ConfirmationTypeCode ConfirmationType, PL.PolicyStage, (SELECT MAX(PremiumId) FROM tblPremium WHERE ValidityTo IS NULL) LastId
                    FROM tblPremium PR 
                    INNER JOIN tblPolicy PL ON PL.PolicyID = PR.PolicyID
                    INNER JOIN tblFamilies F ON F.FamilyID = PL.FamilyID
                    LEFT OUTER JOIN tblPayer P ON P.PayerID = PR.PayerID
                    INNER JOIN tblPayerType PT ON PT.Code = P.PayerType
                    LEFT OUTER JOIN tblConfirmationTypes CT ON CT.ConfirmationTypeCode = F.ConfirmationType
                    WHERE PR.ValidityTo IS NULL
                    AND PL.ValidityTo IS NULL
                    AND F.ValidityTo IS NULL
                    AND P.ValidityTo IS NULL
                    AND PR.PremiumId > {max_id}
                    GROUP BY PR.PayDate, PR.PayType, F.LocationId, PT.Code, CT.ConfirmationTypeCode, PL.PolicyStage

""")
        return self.execute_sql(sql, self.engine_src)


    def transform(self, data):
        self.progress_tracker.update_stage("Transforming...")
        transformed_data = []
        for row in data:
            transformed_data.append({
                "amount": row["Amount"],
                "pay_date": row["PayDate"],
                "pay_type": row["PayType"],
                "location_id": row["LocationId"],
                "payer_type_code": row["PayerTypeCode"],
                "confirmation_type": row["ConfirmationType"] if row["ConfirmationType"] else None,
                "policy_stage": row["PolicyStage"],
                "last_id": row["LastId"]
            })

        return transformed_data


    def load(self, data):
        self.progress_tracker.update_stage("Loading...")
        sql = text("""
                    INSERT INTO premiums (amount, pay_date, pay_type, location_id, payer_type, confirmation_type, policy_stage,  last_id)
                    VALUES(:amount, :pay_date, :pay_type, :location_id, :payer_type_code, :confirmation_type, :policy_stage, :last_id)
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
