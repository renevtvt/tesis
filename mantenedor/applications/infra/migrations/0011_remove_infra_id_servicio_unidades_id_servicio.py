# Generated by Django 5.0.6 on 2024-07-01 01:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infra', '0010_rename_actividad_actividad_cantidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infra',
            name='id_servicio',
        ),
        migrations.AddField(
            model_name='unidades',
            name='id_servicio',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='infra.servicios'),
            preserve_default=False,
        ),
    ]
