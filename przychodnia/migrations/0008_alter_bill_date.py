# Generated by Django 4.0.4 on 2022-05-29 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('przychodnia', '0007_alter_bill_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateTimeField(max_length=100),
        ),
    ]