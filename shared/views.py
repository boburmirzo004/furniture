from django.contrib import messages
from django.shortcuts import render

from shared.forms import ContactForm
from shared.models import AboutUs, Contact


def home_page_view(request):
    return render(request, 'shared/home.html')


def contact_page_view(request):
    if request.method == 'GET':
        return render(request, 'shared/contact.html')
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            text = 'Successfully sent to the admin,thanks  for your attention'
            messages.success(request, text)
        else:
            error_messages = ', '.join([f"{field}: {', '.join(errors)}"
                                        for field, errors in form.errors.items()])
            messages.error(request, error_messages)
        return render(request, 'shared/contact.html')


def about_us_page_view(request):
    context = {
        "abouts": AboutUs.objects.all()
    }
    return render(request, 'shared/about-us.html', context=context)
