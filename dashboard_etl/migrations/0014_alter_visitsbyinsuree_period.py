# Generated by Django 4.2.11 on 2024-03-26 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_etl', '0013_visitsbyinsuree_last_id_alter_visitsbyinsuree_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitsbyinsuree',
            name='period',
            field=models.DateField(db_column='Period', null=True),
        ),
    ]