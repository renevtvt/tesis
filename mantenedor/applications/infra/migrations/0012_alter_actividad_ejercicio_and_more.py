# Generated by Django 5.0.6 on 2024-07-06 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infra', '0011_remove_infra_id_servicio_unidades_id_servicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='ejercicio',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='filiales',
            name='nombre_filial',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='servicios',
            name='nombre_servicio',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
