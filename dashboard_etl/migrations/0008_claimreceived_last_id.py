# Generated by Django 4.2.11 on 2024-03-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_etl', '0007_activeinsuree_last_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='claimreceived',
            name='last_id',
            field=models.IntegerField(db_column='LastId', default=None),
            preserve_default=False,
        ),
    ]
