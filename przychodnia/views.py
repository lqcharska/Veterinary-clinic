from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from przychodnia.forms import AddAnimalForm, AddOwnerForm, WatchOwnerForm, BuyEquipmentForm
from przychodnia.models import Animal, Owner, Bill

from datetime import datetime

def index(request):
    return render(request, 'home.html', {})


def add_owner(request):
    # print(Owner.objects.all().delete())
    # print(Bill.objects.all().delete())
    # print(Animal.objects.all().delete())
    # Variable to handle form errors
    received_errors_dictionary = {}
    error_message = ""
    success_message = ""
    if request.POST:
        received_form = AddOwnerForm(request.POST)

        if received_form.is_valid():
            if len(Owner.objects.filter(name=received_form.cleaned_data['name'])) > 0:
                """
                If user with this data exists, we can not add this data to database
                """
                error_message = f"User {received_form.cleaned_data['name']} exists."
            else:
                """
                User not exists, can be added to database
                """
                received_form.save()
                success_message = f"Successfully saved user {received_form.cleaned_data['name']}"
        else:
            # TODO this should be handled and message printed to user
            # received_errors_dictionary = received_form.errors.as_data()
            error_message = "form is invalid"

    return render(request, 'add_owner.html', {
        'form': AddOwnerForm(),
        'success_message': success_message if success_message != "" else None,  # not used for now
        'error_message': error_message if error_message != "" else None,  # not used for now
    })


def show_owners(request):
    owners = Owner.objects.all()
    return render(request, 'show_owners.html', {
        'owners': owners,
     })


def show_bills(request):
    bills = Bill.objects.all()
    return render(request, 'show_bills.html', {
        'bills': bills,
     })


def show_animals(request):
    animals = Animal.objects.all()
    return render(request, 'show_animals.html', {
        'animals': animals,
     })


def _render_watch_owner(request, owner, success_message, error_message):
    """
    Render page for specified owner with messages
    """

    """
    Find all bills requested by owner
    """
    bills = Bill.objects.filter(owner=owner)

    """
    Find all animals that belengs to the selected owner
    """
    owners_animals = Animal.objects.filter(owner=owner)
    if len(owners_animals) == 0:
        owners_animals = None

    return render(request, 'watch_owner.html', {
        'owner': owner,
        'success_message': success_message if success_message != "" else None,
        'error_message': error_message if error_message != "" else None,
        'owners_animals': owners_animals,
        'bills': bills if len(bills) > 0 else None,
    })


def watch_owner(request):
    success_message = ""
    error_message = ""
    if request.POST and request.POST.get("form_name") == 'buy_equiplent':
        print("received buy fprm")
        received_buy_form = BuyEquipmentForm(request.POST)
        if received_buy_form.is_valid():
            owner = received_buy_form.cleaned_data["owner"]
            animal_id = received_buy_form.cleaned_data["animal_id"]
            product = received_buy_form.cleaned_data["product"]

            bill_model = Bill(owner=owner,
                            animal=Animal.objects.filter(id=animal_id)[0],
                            product=product,
                            date=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            
            bill_model.save()

            return _render_watch_owner(request, owner, success_message, error_message)
        else:
            error_message = str(received_buy_form.errors)
    
    if request.POST and request.POST.get("form_name") == 'add_animal':
        """
        There are more then one possible form, based on 'form_name' the proper one is recognized
        If sb added new animal, the owner is hidden in 'add_animal' form
        Go to 'watch_owner.html' and see the form
        """
        received_animal_form = AddAnimalForm(request.POST)
        if received_animal_form.is_valid():
            """
            Try to find an animal with this name, that belongs to the  selected owner
            """
            animals = Animal.objects.filter(owner=received_animal_form.cleaned_data['owner'],
                                            name=received_animal_form.cleaned_data['name'],
                                            age=received_animal_form.cleaned_data['age']
                                            )
            if animals is not None and len(animals) > 0:
                """
                If this owner have this animal, can not add again the same animal
                """
                error_message = f"This animal exists in database: {received_animal_form.cleaned_data['name']}. You can not add again the same animal."
            else:
                """
                If it is new animal for this owner, it can be added to database.
                """
                received_animal_form.save()
                success_message = f"Successfully added new animal: {received_animal_form.cleaned_data['name']}"

            owner = received_animal_form.cleaned_data['owner']
            return _render_watch_owner(request, owner, success_message, error_message)
        else:
            error_message = str(received_animal_form.errors)

    if request.GET:
        watched_owner = WatchOwnerForm(request.GET)
        if watched_owner.is_valid():
            selected_owner_id = watched_owner.cleaned_data["selected_owner_id"]
            owner = Owner.objects.filter(id=selected_owner_id)
            if len(owner) > 0:
                return _render_watch_owner(request, owner[0], success_message, error_message)

    return redirect('/show_owners')

