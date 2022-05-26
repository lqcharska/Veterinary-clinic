from django.db import models

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


class Animal(models.Model):
    """
    The animal, can be one type of: dog, cat, hamster, guinea pig
    """
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    age = models.IntegerField()
    name = models.CharField(max_length=30)

    type = models.CharField(max_length=1, choices=[
        ('d', 'dog'),
        ('c', 'cat'),
        ('h', 'hamster'),
        ('g', 'guinea pig')
    ])

    def __str__(self):
        return 'name: %s, age: %s, type: %s' % (self.name, self.age, self.type)


class Bill(models.Model):
    """
    Bill for products bought by owner for specified animal 
    """
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

    def __str__(self):
        return 'Animal name %s product %s date %s' % (self.animal.name, self.product, self.date)
