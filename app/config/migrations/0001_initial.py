# Generated by Django 3.2.6 on 2021-11-01 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TAB_Parametro',
            fields=[
                ('prm_empresa', models.CharField(db_column='PRM_Empresa', max_length=2)),
                ('prm_local', models.CharField(db_column='PRM_Local', max_length=2)),
                ('prm_nome', models.CharField(db_column='PRM_Nome', max_length=50, primary_key=True, serialize=False)),
                ('prm_valor', models.CharField(db_column='PRM_Valor', max_length=4000)),
                ('prm_sequencia', models.IntegerField(db_column='PRM_Sequencia')),
                ('prm_incremento', models.IntegerField(db_column='PRM_Incremento')),
                ('prm_valor_max', models.IntegerField(db_column='PRM_Valor_Max')),
                ('prm_categoria', models.CharField(db_column='PRM_Categoria', max_length=20)),
                ('prm_texto', models.CharField(db_column='PRM_Texto', max_length=250)),
                ('prm_criacao', models.DateTimeField(db_column='PRM_Criacao')),
                ('prm_alteracao', models.DateTimeField(db_column='PRM_Alteracao')),
            ],
            options={
                'db_table': 'TAB_Parametro',
                'managed': False,
            },
        ),
    ]