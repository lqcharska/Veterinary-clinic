# Generated by Django 3.2.9 on 2022-05-24 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('date', models.DateField()),
                ('owner_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='przychodnia.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(choices=[('d', 'dog'), ('c', 'cat'), ('h', 'hamster'), ('g', 'guinea pig')], max_length=1)),
                ('owner_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='przychodnia.owner')),
            ],
        ),
    ]