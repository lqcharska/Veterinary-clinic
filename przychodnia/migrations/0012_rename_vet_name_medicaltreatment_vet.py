# Generated by Django 4.0.4 on 2022-06-05 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('przychodnia', '0011_alter_medicaltreatment_vet_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicaltreatment',
            old_name='vet_name',
            new_name='vet',
        ),
    ]