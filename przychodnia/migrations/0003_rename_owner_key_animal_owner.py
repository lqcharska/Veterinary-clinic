# Generated by Django 4.0.4 on 2022-05-25 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('przychodnia', '0002_bill_animal_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal',
            old_name='owner_key',
            new_name='owner',
        ),
    ]