# Generated by Django 4.0.4 on 2022-05-26 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('przychodnia', '0003_rename_owner_key_animal_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='animal_key',
            new_name='animal',
        ),
        migrations.RenameField(
            model_name='bill',
            old_name='owner_key',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='bill',
            old_name='value',
            new_name='product',
        ),
    ]