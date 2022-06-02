from django.db import models
from uuid import uuid4
import os

"""
To create databases based on model classes, 
run 'python manage.py makemigrations' 
and then 'python manage.py migrate'
"""


class Owner(models.Model):
    """
    The Owner of the animal
    """
    phone = models.CharField(max_length=9)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)

    def __str__(self):
        return 'name %s phone %s address %s' % (self.name, self.phone, self.address)

def path_and_rename(instance, filename):
    """
    Form https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload
    """
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Animal(models.Model):
    """
    The animal, can be one type of: dog, cat, hamster, guinea pig
    """
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    age = models.IntegerField()
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True)

    type = models.CharField(max_length=1, choices=[
        ('d', 'dog'),
        ('c', 'cat'),
        ('h', 'hamster'),
        ('g', 'guinea pig'),
        ('z', "snake"),
        ('o', "owl"),
        ('r', "rat"),
        ('t', "house_elf")
    ])

    def __str__(self):
        return 'name: %s, age: %s, type: %s' % (self.name, self.age, self.type)


class MedicalTreatment(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    vet_name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    date = models.DateTimeField(auto_now=True)


class Vet(models.Model):
    name = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)
    image = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True)
