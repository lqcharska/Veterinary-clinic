from django import forms
from django.core.exceptions import ValidationError
from django.forms import models

from przychodnia.models import Animal, Owner, Vet


class WatchOwnerForm(forms.Form):
    selected_owner_id = forms.IntegerField()


class AddOwnerForm(models.ModelForm):
    phone = forms.CharField(max_length=9, required=True)
    name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Owner
        fields = '__all__'


    def clean_phone(self):
        """
        Check if phone is only digits characters,
        it will be checked when is_valid() method is called
        """

        print("cleaning phone dayta")
        phone = self.cleaned_data.get('phone', 0)
        print(phone)

        if not phone.isnumeric():
            print("is not nbmeric")
            raise forms.ValidationError('Phone is not digit')

        return phone

class AddAnimalForm(models.ModelForm):
    owner = forms.ModelChoiceField(queryset=Owner.objects.all())
    # owner = forms.IntegerField(required=True)
    age = forms.IntegerField(required=True)
    name = forms.CharField(max_length=30, required=True)
    type = forms.CharField(max_length=100, required=True)
    image = forms.ImageField()

    class Meta:
        model = Animal
        fields = '__all__'

class MedicalTreatmentFrom(forms.Form):
    owner = forms.ModelChoiceField(queryset=Owner.objects.all())
    animal_id = forms.IntegerField(required=True)
    vet_name = forms.CharField(max_length=100)
    tag = forms.CharField(max_length=100)
    description = forms.CharField(max_length=2000)

class FilterInfoForm(forms.Form):
    selected_page = forms.IntegerField(required=False, initial=1)
    items_per_page = forms.IntegerField(required=False, initial=5)
    start_time = forms.DateTimeField(required=False)
    stop_time = forms.DateTimeField(required=False)
    text_query = forms.CharField(max_length=100, required=False)
        

class AddVetForm(models.ModelForm):
    name = forms.CharField(max_length=50, required=True)
    speciality = forms.CharField(max_length=50, required=True)
    image = forms.ImageField()

    class Meta:
        model = Vet
        fields = '__all__'
