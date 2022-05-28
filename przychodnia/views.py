from tkinter import NO
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from przychodnia.forms import AddAnimalForm, AddOwnerForm, WatchOwnerForm, BuyEquipmentForm, PageSettingsForm
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


class Pages:
    class Button:
        def __init__(self, text, status, value) -> None:
            self.text = text
            self.status = status
            self.value = value
    
    def __init__(self, count: int, name: str) -> None:
        self.count = count
        self.buttons = []
        self.items = []
        self.items_indexes = []
        self.ziped_items = []
        self.name = name

        self.items_per_page = {}
        self.items_per_page["5"] = ""
        self.items_per_page["10"] = ""
        self.items_per_page["15"] = ""
        self.items_per_page["20"] = ""
        

def _get_pages_settings(request):
    selected_page_number = 1
    items_per_page = 5

    if request.GET:
        page_settings = PageSettingsForm(request.GET)
        if page_settings.is_valid():
            temp = page_settings.cleaned_data['selected_page']
            if temp is not None:
                selected_page_number = int(temp)
            
            temp = page_settings.cleaned_data['items_per_page']
            if temp is not None:
                items_per_page = int(temp)
    
    return selected_page_number, items_per_page

def get_page_items(items, items_per_page: int, selected_page_number: int, name: str):
    """
    selected_page_number counts from 1
    """
    total_pages_count = int(int(len(items) / int(items_per_page)) + (1 if (len(items) % items_per_page) > 0 else 0))
    
    print(total_pages_count)
    pages = Pages(total_pages_count, name)


    """
    selected_page_index counts from 0
    """
    selected_page_index = selected_page_number - 1

    if selected_page_index > total_pages_count:
        selected_page_index = total_pages_count
    
    if selected_page_index < 0:
        selected_page_index = 0

    """
    Get selected items to be shown
    """
    start_item_index = selected_page_index * items_per_page
    stop_item_index = min(len(items), start_item_index + items_per_page)
    pages.items = items[start_item_index:stop_item_index]
    pages.items_indexes = list(range(start_item_index + 1, stop_item_index + 1))
    pages.ziped_items = zip(pages.items, pages.items_indexes)
    pages.items_per_page[str(items_per_page)] = "selected"

    """
    Create  buttons
    """
    if total_pages_count > 0:
        pages.buttons.append(Pages.Button(text="Preview", 
                                    status="disabled" if selected_page_number == 1 else "",
                                    value=selected_page_number-1))    
        for i in range(total_pages_count):
            index_on_button = i + 1
            pages.buttons.append(Pages.Button(text=index_on_button, 
                                    status="active" if index_on_button==selected_page_number else "", 
                                    value=index_on_button))

        pages.buttons.append(Pages.Button(text="Next", 
                            status="disabled" if total_pages_count==selected_page_number else "", 
                            value=selected_page_number+1))

    
    return pages


def show_bills(request):
    selected_page_number, items_per_page = _get_pages_settings(request)

    bills = Bill.objects.all()

    return render(request, 'show_bills.html', {
        'bills_and_pages': get_page_items(bills, items_per_page, selected_page_number, "bills")
     })


def show_animals(request):
    selected_page_number, items_per_page = _get_pages_settings(request)

    animals = Animal.objects.all()
    
    return render(request, 'show_animals.html', {
        'animals_and_pages': get_page_items(animals, items_per_page, selected_page_number, "animals")
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

