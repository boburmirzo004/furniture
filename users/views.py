from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render



def account_page_view(request):
    return render(request, 'users/account.html')


def register_page_view(request):

    if request.method == 'GET':
        return render(request, 'users/register.html')

    else:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            text = 'Successfully sent to the admin,thanks  for your attention'
            messages.success(request, text)

        else:
            error_messages = ', '.join([f"{field}: {', '.join(errors)}"
                                        for field, errors in form.errors.items()])
            messages.error(request, error_messages)

        return render(request, 'users/register.html')


def login_page_view(request):
    return render(request, 'users/login.html')


def reset_password_page_view(request):
    return render(request, 'users/reset-password.html')
