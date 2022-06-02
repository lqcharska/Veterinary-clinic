# Generated by Django 4.0.4 on 2022-06-02 21:15

from django.db import migrations, models
import przychodnia.models


class Migration(migrations.Migration):

    dependencies = [
        ('przychodnia', '0009_medicaltreatment_delete_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('speciality', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to=przychodnia.models.path_and_rename)),
            ],
        ),
        migrations.AlterField(
            model_name='animal',
            name='type',
            field=models.CharField(choices=[('d', 'dog'), ('c', 'cat'), ('h', 'hamster'), ('g', 'guinea pig'), ('z', 'snake'), ('o', 'owl'), ('r', 'rat'), ('t', 'house_elf')], max_length=1),
        ),
    ]
