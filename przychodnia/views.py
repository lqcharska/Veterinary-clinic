from tkinter import NO
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from przychodnia.forms import AddAnimalForm, AddOwnerForm, WatchOwnerForm, BuyEquipmentForm, PageSettingsForm
from przychodnia.models import Animal, Owner, Bill

from datetime import datetime

import csv

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
        self.start_item_index = 0
        self.stop_item_index = 0

        self.items_per_page = {}
        self.items_per_page["5"] = ""
        self.items_per_page["10"] = ""
        self.items_per_page["15"] = ""
        self.items_per_page["20"] = ""

def _get_page_items(items, items_per_page: int, selected_page_number: int, name: str):
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
    pages.start_item_index = start_item_index
    pages.stop_item_index = stop_item_index
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

def show_owners(request):
    selected_page_number, items_per_page = _get_pages_settings(request)
    owners = Owner.objects.all()
    return render(request, 'show_owners.html', {
        'owners_and_pages': _get_page_items(owners, items_per_page, selected_page_number, "owners")
     })

def show_bills(request):
    selected_page_number, items_per_page = _get_pages_settings(request)
    bills = Bill.objects.all()

    download_info = {'selected_page_number': selected_page_number, 'items_per_page': items_per_page}
    # download_info = zip(selected_page_number, items_per_page)
    return render(request, 'show_bills.html', {
        'bills_and_pages': _get_page_items(bills, items_per_page, selected_page_number, "bills"),
        'download_info': download_info
    })


def download_bills(request):
    # select 
    selected_page_number, items_per_page = _get_pages_settings(request)

    # get only items which are on page
    page_items = _get_page_items(Bill.objects.all(), items_per_page, selected_page_number, "bills")

    # Create temporary file
    with open('temp.csv', 'w', encoding='UTF8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        bills = Bill.objects.all()[page_items.start_item_index:page_items.stop_item_index]
        writer.writerow(['Index', 'Owner', 'Animal', 'Product', 'Date'])
        index = page_items.start_item_index + 1
        for bill in bills:
            owner = bill.owner.name
            animal = bill.animal.name
            product = bill.product
            date = bill.date

            writer.writerow([index, owner, animal, product, date])
            index = index + 1

        csv_file.close()

    # read and create response
    with open('temp.csv', 'r') as f:
        file_data = f.read()

    response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="temp.csv"'
    return response

def show_animals(request):
    selected_page_number, items_per_page = _get_pages_settings(request)
    animals = Animal.objects.all()
    return render(request, 'show_animals.html', {
        'animals_and_pages': _get_page_items(animals, items_per_page, selected_page_number, "animals")
     })


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
        # Imege upload from: https://djangocentral.com/uploading-images-with-django/
        received_animal_form = AddAnimalForm(request.POST, request.FILES)
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
            print(str(received_animal_form.errors))

    if request.GET:
        watched_owner = WatchOwnerForm(request.GET)
        if watched_owner.is_valid():
            selected_owner_id = watched_owner.cleaned_data["selected_owner_id"]
            owner = Owner.objects.filter(id=selected_owner_id)
            if len(owner) > 0:
                return _render_watch_owner(request, owner[0], success_message, error_message)

    return redirect('/show_owners')

