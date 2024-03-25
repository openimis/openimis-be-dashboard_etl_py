# Generated by Django 4.2.11 on 2024-03-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_etl', '0009_alter_claimreceived_age_alter_claimreceived_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuredhousehold',
            name='last_id',
            field=models.IntegerField(db_column='LastId', default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='insuredhousehold',
            name='age',
            field=models.IntegerField(db_column='Age', null=True),
        ),
        migrations.AlterField(
            model_name='insuredhousehold',
            name='policy_stage',
            field=models.CharField(db_column='PolicyStage', max_length=1, null=True),
        ),
    ]