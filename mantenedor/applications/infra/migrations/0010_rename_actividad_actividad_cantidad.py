# Generated by Django 5.0.6 on 2024-07-01 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infra', '0009_alter_infra_hora'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actividad',
            old_name='actividad',
            new_name='cantidad',
        ),
    ]
