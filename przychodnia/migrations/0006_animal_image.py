# Generated by Django 4.0.4 on 2022-05-28 16:52

from django.db import migrations, models
import przychodnia.models


class Migration(migrations.Migration):

    dependencies = [
        ('przychodnia', '0005_alter_bill_date_alter_bill_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=przychodnia.models.path_and_rename),
        ),
    ]
