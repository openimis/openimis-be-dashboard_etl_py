from django.apps import AppConfig
import os
from django.db.models.signals import post_migrate
from django.core import management

class DashboardConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard_etl'
    batch_size = 25000
    src_con_str = f'{os.environ.get("DB_ENGINE")}+pyodbc://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}?driver=ODBC+Driver+17+for+SQL+Server'
    dest_con_str = f'{os.environ.get("DASHBOARD_DB_ENGINE")}+pyodbc://{os.environ.get("DASHBOARD_DB_USER")}:{os.environ.get("DASHBOARD_DB_PASSWORD")}@{os.environ.get("DASHBOARD_DB_HOST")}:{os.environ.get("DASHBOARD_DB_PORT")}/{os.environ.get("DASHBOARD_DB_NAME")}?driver=ODBC+Driver+17+for+SQL+Server'

    indicators = [
        ("active_households"),
        ("active_insurees"),
    ]


    def ready(self) -> None:
        post_migrate.connect(self.start_celery_worker, sender=self)

    def start_celery_worker(self, **kwargs):
        management.call_command('celery', 'worker', '--detach', '--loglevel=info', '--pool=thread')