from django.core.exceptions import ValidationError
from django.shortcuts import render

# Create your views here.
from przychodnia.forms import AddOwnerForm
from przychodnia.models import Owner


def index(request):
    return render(request, 'home.html', {})


def add_owner_form(request):
    # print(Owner.objects.all().delete())
    # Variable to handle form errors
    received_errors_dictionary = {}
    error_message = ""
    success_message = ""
    if request.POST:
        received_form = AddOwnerForm(request.POST)

        if received_form.is_valid():
            if len(Owner.objects.filter(name=received_form.cleaned_data['name'],
                                        phone=received_form.cleaned_data['phone'],
                                        address=received_form.cleaned_data['address'])) > 0:
                """
                If user with this data exists, we can not add this data to database
                """
                error_message = "User exists"
            else:
                """
                User not exists, can be added to database
                """
                received_form.save()
                success_message = "Successfully saved owner data"
        else:
            # TODO this should be handled and message printed to user
            # received_errors_dictionary = received_form.errors.as_data()
            error_message = "form is invalid"

    return render(request, 'add_owner.html', {
        'form': AddOwnerForm(),
        'success_message': success_message if success_message != "" else None,  # not used for now
        'error_message': error_message if error_message != "" else None,  # not used for now
    })
