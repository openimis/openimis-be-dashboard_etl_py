import asyncio
from decimal import Decimal
from dashboard_etl.extract.progress import ETLProgress
from django.apps import apps
from django.db import connection
from django.db.models import Max
from django.core.cache import cache
from dashboard_etl.models import ActiveHousehold
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .etl_base import ETLBase

BATCH_SIZE = apps.get_app_config("dashboard_etl").batch_size
source_con_str = apps.get_app_config("dashboard_etl").src_con_str
dest_con_str = apps.get_app_config("dashboard_etl").dest_con_str
INDICATOR = "active_households"


class ActiveHouseholdExtractor(ETLBase):

    def __init__(self) -> None:
        self.progress_tracker = ETLProgress(INDICATOR)
        self.engine_src = create_engine(source_con_str)
        self.engine_dest = create_engine(dest_con_str, fast_executemany=True)

    def execute_sql(self, sql, engine):
        # with AsyncSession(engine) as session:
        #     result = session.execute(sql)
        #     return result.all()
        with engine.connect() as conn:
            result = conn.execute(sql)
            return result.mappings().all()

    def run_etl(self):
        extracted_data = self.extract()
        transformed_data = self.transform(extracted_data)
        self.load(transformed_data)

    def get_max_last_id(self):
        # max_last_id = ActiveHousehold.objects.using(DATABASE).aggregate(max_last_id=Max("last_id"))
        # return max_last_id["max_last_id"] or 0
        sql = text("SELECT ISNULL(MAX(LastId), 0) LastId FROM ActiveHouseholds")
        max_id = self.execute_sql(sql, self.engine_dest)
        return max_id[0]["LastId"]

    def extract(self):

        print("Extracting...")
        self.progress_tracker.update_stage("Extracting...")
        max_id = self.get_max_last_id()

        sql = text(f"""
            SELECT TOP 100000 COUNT(DISTINCT F.FamilyID) ActiveHouseholds, DATEADD(MONTH, MonthNumber.Number, InsP.EffectiveDate) ActivePeriod, F.LocationId, I.Gender, DATEDIFF(DAY, I.DOB, InsP.EffectiveDate)/365 Age, F.ConfirmationType, SUM(P.PolicyValue)BenefitAmount, (SELECT MAX(InsureePolicyId) FROM tblInsureePolicy WHERE ValidityTo IS NULL)LastId
            FROM tblInsureePolicy InsP
            INNER JOIN tblInsuree I ON I.InsureeId = InsP.InsureeId
            INNER JOIN tblFamilies F ON F.InsureeID = I.InsureeID
            INNER JOIN tblLocations L ON L.LocationId = F.LocationId
            INNER JOIN tblPolicy P ON P.FamilyID = F.FamilyID
            CROSS APPLY (VALUES(0), (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),(11), (12))MonthNumber(Number)
            WHERE InsP.ValidityTo IS NULL
            AND I.ValidityTo IS NULL
            AND F.ValidityTo IS NULL
            AND L.ValidityTo IS NULL
            AND P.ValidityTo IS NULL
            AND InsP.InsureePolicyId > {max_id}
            GROUP BY DATEADD(MONTH, MonthNumber.Number, InsP.EffectiveDate), F.LocationId, I.Gender, DATEDIFF(DAY, I.DOB, InsP.EffectiveDate)/365, F.ConfirmationType

""")
        # sql = text(f"""SELECT TOP 100000 3 ActiveHouseholds, InsP.EffectiveDate ActivePeriod, F.LocationId, I.Gender, DATEDIFF(DAY, InsP.EffectiveDate, I.DOB)/365 Age, F.ConfirmationType, 0 BenefitAmount, 0 LastId
        #             FROM tblInsureePolicy InsP
        #             INNER JOIN tblInsuree I ON I.InsureeId = InsP.InsureeId
        #             INNER JOIN tblFamilies F ON F.FamilyID = I.FamilyID
        #             WHERE InsP.ValidityTo IS NULL
        #             AND I.ValidityTo IS NULL
        #             AND F.ValidityTo IS NULL
        #             AND I.IsHead = 1""")


        # with connection.cursor() as cursor:
        #     cursor.execute(sql)
        #     return cursor.fetchall()

        return self.execute_sql(sql, self.engine_src)


    def transform(self, data):
        print("transforming...")
        self.progress_tracker.update_stage("Transforming...")
        transformed_data = []
        for row in data:
            transformed_data.append({
                "active_households": row["ActiveHouseholds"],
                "period": row["ActivePeriod"],
                "location_id": row["LocationId"],
                "gender": row["Gender"],
                "age": row["Age"],
                "confirmation_type": row["ConfirmationType"] if row["ConfirmationType"] else None,
                "benefit_amount": row["BenefitAmount"],
                "last_id": row["LastId"]
            })

        return transformed_data


    def load(self, data):
        self.progress_tracker.update_stage("Loading...")
        sql = text("INSERT INTO ActiveHouseholds(ActiveHouseholds, ActivePeriod, LocationId, Gender, Age, ConfirmationType, BenefitAmount, LastId) VALUES(:active_households, :period, :location_id, :gender, :age, :confirmation_type, :benefit_amount, :last_id)")

        page = 0
        total_pages = (len(data) + BATCH_SIZE - 1) // BATCH_SIZE

        with self.engine_dest.connect() as conn:
            for i in range(0, len(data), BATCH_SIZE):
                page += 1
                batch = data[i: i + BATCH_SIZE]
                data_to_insert = [{**row} for row in batch]
                conn.execute(sql, data_to_insert)
                print(f"Page {page}/{total_pages}")
                self.progress_tracker.update_stage(f"{(((Decimal(page)/total_pages)) * 100):.2f}% completed")

        # with self.engine_dest.begin() as conn:
        #     for i in range(0, len(data), BATCH_SIZE):
        #         page += 1

        #         batch = data[i: i + BATCH_SIZE]
        #         data_to_insert = [{**row} for row in batch]
        #         conn.execute(sql, data_to_insert)
        #         conn.commit()
        #         print(f"Page {page}/{total_pages}")
        #         self.progress_tracker.update_stage(f"{(((Decimal(page)/total_pages)) * 100):.2f}% completed")

            conn.commit()
