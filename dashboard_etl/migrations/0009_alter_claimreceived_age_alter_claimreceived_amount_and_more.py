# Generated by Django 4.2.11 on 2024-03-25 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_etl', '0008_claimreceived_last_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimreceived',
            name='age',
            field=models.IntegerField(blank=True, db_column='Age', null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='amount',
            field=models.DecimalField(blank=True, db_column='Amount', decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='approved',
            field=models.DecimalField(blank=True, db_column='Approved', decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='care_type',
            field=models.CharField(blank=True, db_column='CareType', max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='claim_status',
            field=models.IntegerField(blank=True, db_column='ClaimStatus', null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='hf_days',
            field=models.IntegerField(blank=True, db_column='DaysInHF', null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='last_id',
            field=models.IntegerField(blank=True, db_column='LastId', null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='processing_days',
            field=models.IntegerField(blank=True, db_column='ProcessingDays', null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='review_status',
            field=models.IntegerField(blank=True, db_column='ReviewStatus', null=True),
        ),
        migrations.AlterField(
            model_name='claimreceived',
            name='visit_type',
            field=models.CharField(blank=True, db_column='VisitType', max_length=1, null=True),
        ),
    ]