# Generated by Django 3.2.6 on 2021-10-13 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id_paciente', models.CharField(db_column='Pat_ID1', max_length=250, primary_key=True, serialize=False)),
                ('firstname', models.CharField(blank=True, db_column='First_Name', max_length=250, null=True)),
                ('lastname', models.CharField(blank=True, db_column='Last_Name', max_length=250, null=True)),
                ('datanasc', models.DateTimeField(blank=True, db_column='Birth_DtTm', null=True)),
            ],
            options={
                'db_table': 'Patient',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id_agenda', models.IntegerField(db_column='Sch_Id', primary_key=True, serialize=False)),
                ('dataagenda', models.DateTimeField(blank=True, db_column='App_DtTm', null=True)),
                ('status', models.CharField(blank=True, db_column='SchStatus_Hist_SD', max_length=250, null=True)),
            ],
            options={
                'db_table': 'Schedule',
                'managed': False,
            },
        ),
    ]