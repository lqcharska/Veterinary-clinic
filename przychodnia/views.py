from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from przychodnia.forms import AddOwnerForm, WatchOwnerForm
from przychodnia.models import Owner


def index(request):
    return render(request, 'home.html', {})


def add_owner(request):
    # print(Owner.objects.all().delete())
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


def watch_owner(request):
    if request.GET:
        watch_owner = WatchOwnerForm(request.GET)
        if watch_owner.is_valid():
            selected_owner_id = watch_owner.cleaned_data["selected_owner_id"]
            owner = Owner.objects.filter(id=selected_owner_id)
            if len(owner) > 0:
                owner = owner[0]
                return render(request, 'watch_owner.html', {
                    'owner': owner,
                 })
            else:
                return redirect('show_owners')
