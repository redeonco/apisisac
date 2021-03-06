# Generated by Django 3.2.6 on 2021-10-14 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_entrada'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entradaradio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codmovimento', models.CharField(blank=True, db_column='CodMovimento', max_length=10, null=True)),
                ('codpaciente', models.CharField(blank=True, db_column='CodPaciente', max_length=10, null=True)),
                ('idplanejfisico', models.CharField(blank=True, db_column='idPlanejFisico', max_length=10, null=True)),
                ('encerrado', models.CharField(blank=True, db_column='Encerrado', max_length=10, null=True)),
                ('observacao', models.CharField(blank=True, db_column='Observacao', max_length=200, null=True)),
                ('usuario', models.CharField(blank=True, db_column='Usuario', max_length=20, null=True)),
                ('datahora', models.DateTimeField(blank=True, db_column='DataHora', null=True)),
                ('datasist', models.DateTimeField(blank=True, db_column='DataSist', null=True)),
                ('nplanejamento', models.IntegerField(blank=True, db_column='NPlanejamento', null=True)),
                ('nomecampo', models.CharField(blank=True, db_column='NomeCampo', max_length=100, null=True)),
                ('incidencia', models.CharField(blank=True, db_column='Incidencia', max_length=50, null=True)),
                ('grupoemp', models.CharField(blank=True, db_column='GrupoEmp', max_length=2, null=True)),
                ('filial', models.CharField(blank=True, db_column='Filial', max_length=2, null=True)),
                ('ntratamento', models.IntegerField(blank=True, db_column='NTratamento', null=True)),
                ('ncampo', models.IntegerField(blank=True, db_column='NCampo', null=True)),
            ],
            options={
                'db_table': 'EntradaRadio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Planejfisico',
            fields=[
                ('idplanejfisico', models.CharField(db_column='idPlanejFisico', max_length=10, primary_key=True, serialize=False)),
                ('codpaciente', models.CharField(blank=True, db_column='CodPaciente', max_length=11, null=True)),
                ('incidencia', models.CharField(blank=True, db_column='Incidencia', max_length=50, null=True)),
                ('nomecampo', models.CharField(blank=True, db_column='NomeCampo', max_length=100, null=True)),
                ('nplanejamento', models.IntegerField(blank=True, db_column='NPlanejamento', null=True)),
                ('ntratamento', models.IntegerField(blank=True, db_column='NTratamento', null=True)),
                ('ncampo', models.IntegerField(blank=True, db_column='NCampo', null=True)),
                ('fase', models.IntegerField(blank=True, db_column='Fase', null=True)),
            ],
            options={
                'db_table': 'PlanejFisico',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Radioterapia',
            fields=[
                ('numpresc', models.CharField(db_column='NumPresc', max_length=10, primary_key=True, serialize=False)),
                ('codcidp', models.CharField(blank=True, db_column='CodCidP', max_length=10, null=True)),
                ('estadio', models.CharField(blank=True, db_column='Estadio', max_length=15, null=True)),
                ('finalidade', models.CharField(blank=True, db_column='Finalidade', max_length=20, null=True)),
                ('intencaoradical', models.BooleanField(blank=True, db_column='IntencaoRadical', null=True)),
                ('intencaopaliativa', models.BooleanField(blank=True, db_column='IntencaoPaliativa', null=True)),
                ('tipot', models.CharField(blank=True, db_column='TipoT', max_length=10, null=True)),
                ('tipon', models.CharField(blank=True, db_column='TipoN', max_length=10, null=True)),
                ('tipom', models.CharField(blank=True, db_column='TipoM', max_length=10, null=True)),
                ('naplicacoes', models.IntegerField(blank=True, db_column='NAplicacoes', null=True)),
                ('karno', models.CharField(blank=True, db_column='Karno', max_length=5, null=True)),
                ('codmed', models.CharField(blank=True, db_column='CodMed', max_length=10, null=True)),
            ],
            options={
                'db_table': 'Radioterapia',
                'managed': False,
            },
        ),
    ]
