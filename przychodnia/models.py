from django.db import models


class Owner(models.Model):
    phone = models.CharField(max_length=9)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)


class Animal(models.Model):
    owner_key = models.ForeignKey(Owner, on_delete=models.CASCADE)
    age = models.IntegerField()
    name = models.CharField(max_length=30)

    type = models.CharField(max_length=1, choices=[
        ('d', 'dog'),
        ('c', 'cat'),
        ('h', 'hamster'),
        ('g', 'guinea pig')
    ])


class Bill(models.Model):
    owner_key = models.ForeignKey(Owner, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField()
